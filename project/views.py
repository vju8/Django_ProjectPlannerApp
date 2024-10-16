from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages 
from django.db import IntegrityError

from .models import Project, ProjectFile
from .forms import ProjectFileForm
from task.models import Task


@login_required
def project_list(request):
    projects = Project.objects.filter(created_by=request.user)
    return render(request, 'project/project_list.html', {'projects':projects})


@login_required
def add_project(request):
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        urgency = request.POST['urgency']

        try:
            # create new project 
            project = Project.objects.create(name=name, 
                                                description=description, 
                                                created_by=request.user, 
                                                urgency=urgency)
            # load all existing projects for user
            projects = Project.objects.filter(created_by=request.user)

            # TODO: add 3 buckets based on urgency
            # projects_low = Project.objects.filter(created_by=request.user, urgency='low')
            # projects_medium = Project.objects.filter(created_by=request.user, urgency='medium')
            # projects_high = Project.objects.filter(created_by=request.user, urgency='high')

            messages.success(request, "New Project was created successfully!")
            return render(request, 'project/project_list.html', {'projects':projects})
        except IntegrityError:    
            messages.error(request, "A project with this name already exists.")
            return redirect('project:add_project')
    else: 
        return render(request, 'project/add_project.html')


@login_required
def project_details(request, pk_project):
    project = Project.objects.filter(created_by=request.user).get(id=pk_project)
    tasks = Task.objects.filter(project=project)
    tasks_count = tasks.count()
    tasks_completed = tasks.filter(completed=True).count()
    progress = ((tasks_completed / tasks_count) * 100) if tasks_count > 0 else 0
    project_files = ProjectFile.objects.filter(project=project)
    return render(request, 'project/project_details.html', {"project":project, 
                                                            'tasks':tasks, 
                                                            'tasks_count':tasks_count,
                                                            'tasks_completed':tasks_completed,
                                                            'progress':progress,
                                                            'project_files':project_files})


@login_required
def edit_project(request, pk_project): 
    project = Project.objects.filter(created_by=request.user).get(id=pk_project)

    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        urgency = request.POST['urgency']
        # Check if checkbox is checked (returns 'on' if checked, None if not)
        description_show = request.POST.get('description_show') == 'on'

        try:
            project.name = name 
            project.description = description
            project.urgency = urgency
            project.description_show = description_show
            project.save()
            # load all existing projects for user
            projects = Project.objects.filter(created_by=request.user)
            messages.success(request, "Project edited successfully!")
            return render(request, 'project/project_list.html', {'projects':projects})
        except IntegrityError:
            projects = Project.objects.filter(created_by=request.user)
            messages.error(request, "A project with this name already exists.")
            return render(request, 'project/edit_project.html', {'project':project})      
    return render(request, 'project/edit_project.html', {"project":project})

    
@login_required
def delete_project(request, pk_project): 
    project = Project.objects.filter(created_by=request.user).get(id=pk_project)
    if request.method == "POST":
        project.delete()
        # load all existing projects for user
        projects = Project.objects.filter(created_by=request.user)
        messages.success(request, "Project deleted successfully!")
        return render(request, 'project/project_list.html', {'projects':projects})
    return render(request, 'project/project_details.html', {"project":project})

    
@login_required
def complete_project(request, pk_project): 
    project = Project.objects.filter(created_by=request.user).get(id=pk_project)
    if request.method == "POST":
        # handle complete & undo completion
        if project.completed:
            project.completed = False
        else: 
            project.completed = True
        project.save()
        # load all existing projects for user
        projects = Project.objects.filter(created_by=request.user)
        messages.success(request, "Project completed successfully!")
    return render(request, 'project/project_list.html', {"projects":projects})

    
@login_required
def upload_file(request, pk_project):
    project = Project.objects.filter(created_by=request.user).get(id=pk_project)
    projects = Project.objects.filter(created_by=request.user)
    project_files = ProjectFile.objects.filter(project=project)
    tasks = Task.objects.filter(project=project)
    tasks_count = tasks.count()
    tasks_completed = tasks.filter(completed=True).count()
    progress = ((tasks_completed / tasks_count) * 100) if tasks_count > 0 else 0

    if request.method == "POST":
        form = ProjectFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Don't commit immediately to associate with project
            project_file = form.save(commit=False)
            project_file.project = project  # Assign the project to the file
            project_file.save()
            messages.success(request, "File uploaded successfully!")
        else:
            messages.error(request, "There was an error with your file. Please try again.")
        return render(request, 'project/project_details.html', {'project':project,
                                                                'projects':projects, 
                                                                'tasks':tasks,
                                                                'tasks_count':tasks_count,
                                                                'tasks_completed':tasks_completed,
                                                                'progress':progress,
                                                                'project_files':project_files})
    else:
        form = ProjectFileForm()  # Display empty form for GET request
    return render(request, 'project/project_details.html', {'projects':projects, 
                                                            'project_files':project_files,
                                                            'form':form})

    
@login_required
def delete_attachment(request, pk_project, pk_project_file):
    project = Project.objects.filter(created_by=request.user).get(id=pk_project)
    projects = Project.objects.filter(created_by=request.user)
    tasks = Task.objects.filter(project=project)
    tasks_count = tasks.count()
    tasks_completed = tasks.filter(completed=True).count()
    progress = ((tasks_completed / tasks_count) * 100) if tasks_count > 0 else 0
    # handle the project file deletion
    project_file = ProjectFile.objects.filter(id=pk_project_file)
    project_file.delete()
    project_files = ProjectFile.objects.filter(project=project)
    messages.success(request, "File deleted successfully!")
    return render(request, 'project/project_details.html', {'project':project,
                                                            'projects':projects, 
                                                            'tasks':tasks,
                                                            'tasks_count':tasks_count,
                                                            'tasks_completed':tasks_completed,
                                                            'progress':progress,
                                                            'project_files':project_files})
