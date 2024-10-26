from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from project.models import Project 
from task.models import Task

import plotly.graph_objects as go


@login_required
def index(request): 
    def create_project_chart():
        projects = Project.objects.filter(created_by=request.user)
        projects_completed = projects.filter(completed=True).count()
        projects_uncompleted = projects.filter(completed=False).count()
        # labels, values, colors
        project_labels = ['Completed', 'Uncompleted']
        project_values = [projects_completed, projects_uncompleted]
        project_colors  = ["#192841", "#8DA9C4"]
        # create figure
        project_fig = go.Figure(data=[go.Pie(labels=project_labels, 
                                    values=project_values, 
                                    marker=dict(colors=project_colors), 
                                    textinfo='percent',  # Display both labels and percentages
                                    insidetextfont=dict(size=20),
                                    outsidetextfont=dict(size=20),
                                    hoverinfo='label+value+percent',  
                                    hoverlabel=dict(font=dict(size=20))
                                    )])
        # Adjust layout
        project_fig.update_layout(
            title='Project Statistics',  
            font=dict(size=26, color='black', family='Arial', weight='bold'),
            title_x=0.5,  # Center title
            legend=dict(font=dict(size=20))
        )
        project_chart = project_fig.to_html()
        return project_chart

    def create_task_chart():
        tasks = Task.objects.filter(created_by=request.user)
        tasks_completed = tasks.filter(completed=True).count()
        tasks_uncompleted = tasks.filter(completed=False).count()
        # labels, values, colors
        task_labels = ['Completed', 'Uncompleted']
        task_values = [tasks_completed, tasks_uncompleted]  
        task_colors = ["#192841", "#8DA9C4"]  
        # create figure
        task_fig = go.Figure(data=[go.Pie(labels=task_labels, 
                                        values=task_values, 
                                        marker=dict(colors=task_colors),
                                        textinfo='percent', 
                                        insidetextfont=dict(size=20),
                                        outsidetextfont=dict(size=20),
                                        hoverinfo='label+value+percent',  
                                        hoverlabel=dict(font=dict(size=20))
                                        )])
        # Adjust layout
        task_fig.update_layout(
            title='Task Statistics',  
            font=dict(size=26, color='black', family='Arial', weight='bold'),
            title_x=0.5,  # Center title
            legend=dict(font=dict(size=20)))
        task_chart = task_fig.to_html()
        return task_chart
    
    return render(request, 'core/index.html', {'project_chart': create_project_chart(), 'task_chart': create_task_chart()})



