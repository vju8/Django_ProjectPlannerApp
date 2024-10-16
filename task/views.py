from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages 

from project.models import ProjectFile
from .models import Project, Task 



@login_required
def add_task(request, pk_project): 
    project = Project.objects.filter(created_by=request.user).get(id=pk_project)
    project_files = ProjectFile.objects.filter(project=project)
    if request.method == "POST":
        name = request.POST['name']
        # create task
        Task.objects.create(created_by=request.user, project=project, name=name)

        # handle complete & undo completion
        if project.completed:
            project.completed = False
        else: 
            project.completed = True
        project.save()

        # reload tasks
        tasks = Task.objects.filter(created_by=request.user, project=project)
        tasks_count = tasks.count()
        tasks_completed = tasks.filter(completed=True).count()
        progress = ((tasks_completed / tasks_count) * 100) if tasks_count > 0 else 0
        messages.success(request, "Task added successfully!")
        return render(request, 'project/project_details.html', {'project':project, 
                                                                'tasks':tasks,
                                                                'tasks_count': tasks_count, 
                                                                'tasks_completed':tasks_completed, 
                                                                'progress':progress,
                                                                'project_files':project_files})
    return render(request, 'task/add_task.html', {'project':project})

    
@login_required
def edit_task(request, pk_project, pk_task):
    project = Project.objects.filter(created_by=request.user).get(id=pk_project)
    task = Task.objects.filter(project=project).get(id=pk_task)
    tasks = Task.objects.filter(created_by=request.user, project=project)
    tasks_count = tasks.count() 
    tasks_completed = tasks.filter(completed=True).count()
    progress = ((tasks_completed / tasks_count) * 100) if tasks_count > 0 else 0
    project_files = ProjectFile.objects.filter(project=project)
    
    if request.method == "POST":
        name = request.POST['name']
        task.name = name 
        task.save() 
        messages.success(request, "Task edited successfully!")
        return render(request, 'project/project_details.html', {'project':project, 
                                                                'tasks':tasks,
                                                                'tasks_count': tasks_count, 
                                                                'tasks_completed':tasks_completed, 
                                                                'progress':progress,
                                                                'project_files':project_files})
    return render(request, 'task/edit_task.html', {'project':project, 'task':task})


@login_required
def delete_task(request, pk_project, pk_task):
    project = Project.objects.filter(created_by=request.user).get(id=pk_project)
    task = Task.objects.filter(project=project).get(id=pk_task)
    task.delete()
    tasks = Task.objects.filter(created_by=request.user, project=project)
    tasks_count = tasks.count() 
    tasks_completed = tasks.filter(completed=True).count()
    progress = ((tasks_completed / tasks_count) * 100) if tasks_count > 0 else 0
    project_files = ProjectFile.objects.filter(project=project)
    messages.success(request, "Task deleted successfully!")
    return render(request, 'project/project_details.html', {'project':project, 
                                                            'tasks':tasks,
                                                            'tasks_count': tasks_count, 
                                                            'tasks_completed':tasks_completed, 
                                                            'progress':progress,
                                                            'project_files':project_files})


@login_required
def complete_task(request, pk_project, pk_task):
    project = Project.objects.filter(created_by=request.user).get(id=pk_project)
    task = Task.objects.filter(project=project).get(id=pk_task)

    if task.completed: 
        task.completed = False 
    else:
        messages.success(request, "Task completed successfully!")
        task.completed = True  
    task.save()
    tasks = Task.objects.filter(created_by=request.user, project=project)
    tasks_count = tasks.count() 
    tasks_completed = tasks.filter(completed=True).count()
    progress = ((tasks_completed / tasks_count) * 100) if tasks_count > 0 else 0
    project_files = ProjectFile.objects.filter(project=project)
    return render(request, 'project/project_details.html', {'project':project, 
                                                            'tasks':tasks, 
                                                            'tasks_count': tasks_count, 
                                                            'tasks_completed':tasks_completed, 
                                                            'progress':progress,
                                                            'project_files':project_files})
