from django.db import models 
from django.contrib.auth import get_user_model

# from account.models import AppUser, User

# Use get_user_model() to refer to the custom user model
User = get_user_model()

# DB Model for the Project
class Project(models.Model): 
    """This is a list of tuples where each tuple consists of two elements: 
    the first is the value that will be stored in the database, and the 
    second is the human-readable name that will be displayed in forms 
    and admin interfaces."""
    URGENCY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    BUCKET_CHOICES = [
        ('active', 'Working On'),
        ('completed', 'Completed'),
        ('backlog', 'Backlog'),
    ]

    # id assigned automatically (set as PK)
    name = models.CharField(max_length=50)  
    description = models.TextField(blank=True, null=True)   
        # blank=True allows the field to be empty in forms, null=True allows the field to be NULL in the database 
    created_by = models.ForeignKey(User, related_name="projects", on_delete=models.CASCADE)   
        # related_name="projects" allows you to access the projects related to an AppUser instance using user_instance.projects.all()    
        # on_delete=models.CASCADE means that if the user (creator) is deleted from the database, all their associated projects will also be deleted. This maintains referential integrity in the database.
    created_on = models.DateTimeField(auto_now_add=True)
        # Automatically set to current date and time when created
    urgency = models.CharField(max_length=6, choices=URGENCY_CHOICES, default='low')
        # choices=URGENCY_CHOICES limits the choices for this field
    completed = models.BooleanField(blank=True, default=False)
    description_show = models.BooleanField(blank=True, default=False)
    bucket = models.CharField(max_length=9, choices=URGENCY_CHOICES, default='active')

    # TODO: add additional 2 fields 
    # started_on = models.DateTimeField(blank=True, null=True)
    # due_on = models.DateTimeField(blank=True, null=True)
    

    # add constraint so that the project name is unique per user (two different users allowed to have projects with same name)
    class Meta:
        
        constraints = [
            models.UniqueConstraint(fields=['name', 'created_by'], name='unique_project_per_user')
        ]
    
    def __str__(self):
        return self.name 



class ProjectFile(models.Model): 
    name = models.CharField(max_length=100)
    attachment = models.FileField(upload_to='project_files')   
    project = models.ForeignKey(Project, related_name='files', on_delete=models.CASCADE)
    
    def __str__(self): 
        return self.name 