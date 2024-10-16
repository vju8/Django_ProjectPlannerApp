from django.db import models
from django.contrib.auth import get_user_model
from project.models import Project

# Use get_user_model() to refer to the custom user model
User = get_user_model()


# Create your models here.
class Task(models.Model): 
    # id assigned automatically (set as PK)
    name = models.CharField(max_length=50)  
    project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="tasks", on_delete=models.CASCADE)   
        # related_name="projects" allows you to access the projects related to an AppUser instance using user_instance.projects.all()    
        # on_delete=models.CASCADE means that if the user (creator) is deleted from the database, all their associated projects will also be deleted. This maintains referential integrity in the database.
    created_on = models.DateTimeField(auto_now_add=True)
        # Automatically set to current date and time when created
    completed = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.name 
