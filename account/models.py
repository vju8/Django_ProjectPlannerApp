from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 

from django import forms 



class AppUser(UserCreationForm): 
    first_name = forms.CharField(required=True,
                                 label="First Name", 
                                 max_length=100, 
                                 widget=forms.TextInput(attrs={"class": "form-control",
                                                               "placeholder": "First Name"})
    )
    last_name = forms.CharField(required=True,
                                label="Last Name", 
                                max_length=100, 
                                widget=forms.TextInput(attrs={"class": "form-control",
                                                              "placeholder": "Last Name"})
    )
    username = forms.CharField(required=True,
                               label="Username", 
                               max_length=100, 
                               widget=forms.TextInput(attrs={"class": "form-control",
                                                             "placeholder": "Username"})
    )
    email = forms.EmailField(required=True,
                             label="Email Adress", 
                             max_length=100, 
                             widget=forms.TextInput(attrs={"class": "form-control",
                                                           "placeholder": "Email Adress"})
    )
    password1 = forms.CharField(required=True,
                                label="Password", 
                                max_length=100, 
                                widget=forms.PasswordInput(attrs={"class": "form-control",
                                                                  "placeholder": "Password"})
    )
    password2 = forms.CharField(required=True,
                                label="Repeat Password", 
                                max_length=100, 
                                widget=forms.PasswordInput(attrs={"class": "form-control",
                                                                  "placeholder": "Repeat Password"})
    )
    
    class Meta:
        model = User 
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email
    
    def save(self, commit=True):
        user = super(AppUser, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
