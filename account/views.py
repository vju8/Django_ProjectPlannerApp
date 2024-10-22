from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from .models import AppUser
from django.contrib.auth.models import User



def signup_user(request):
    if request.method == "POST":
        form = AppUser(request.POST)

        # perform authentication
        if form.is_valid():
            form.save() 
            messages.success(request, "Your account has been created successfully!")
            return redirect('account:login_user')
        else:
            messages.error(request, "Wrong registration credentials.")
            return render(request, 'account/signup_user.html', {'form': form})
    else:
        form = AppUser()
        return render(request, 'account/signup_user.html', {'form':form})


def login_user(request): 
    if request.method == "POST": 
        username_or_email = request.POST['username_or_email'] 
        password = request.POST['password']

        try:
            # flexible login with username or email
            if "@" in username_or_email: 
                user = User.objects.get(email=username_or_email)
            else: 
                user = User.objects.get(username=username_or_email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None 

        # authentication
        if user is not None: 
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('core:index')
        else: 
            messages.error(request, "Wrong email and password combination.")
            return render(request, 'account/login_user.html')
    else:
        return render(request, 'account/login_user.html', {})


def logout_user(request): 
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('core:index') 
    