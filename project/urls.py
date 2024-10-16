from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'project'

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('add_project/', views.add_project, name='add_project'),
    path('project_details/<int:pk_project>/', views.project_details, name='project_details'),
    path('edit_project/<int:pk_project>/', views.edit_project, name='edit_project'),
    path('delete_project/<int:pk_project>/', views.delete_project, name='delete_project'),
    path('complete_project/<int:pk_project>/', views.complete_project, name='complete_project'),
    path('upload_file/<int:pk_project>/', views.upload_file, name='upload_file'),
    path('delete_attachment/<int:pk_project>/<int:pk_project_file>/', views.delete_attachment, name='delete_attachment'),
] 