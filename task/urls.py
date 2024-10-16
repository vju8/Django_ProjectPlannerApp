from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'task'

urlpatterns = [
    path('add_task/', views.add_task, name='add_task'),
    path('edit_task/<int:pk_task>/', views.edit_task, name='edit_task'),
    path('delete_task/<int:pk_task>/', views.delete_task, name='delete_task'),
    path('complete_task/<int:pk_task>/', views.complete_task, name='complete_task'),
] 
