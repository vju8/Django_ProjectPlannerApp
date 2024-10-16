from django.forms import ModelForm 

from .models import ProjectFile


class ProjectFileForm(ModelForm):
    class Meta: 
        model = ProjectFile
        fields = ('attachment',)

    def save(self, commit=True):
        # Get the instance but don't save yet
        instance = super().save(commit=False)
        
        # Automatically set the `name` field as the file's name
        instance.name = self.cleaned_data['attachment'].name

        if commit:
            instance.save()
        
        return instance