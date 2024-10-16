from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from account.models import AppUser




# Create your views here.
def index(request): 
    return render(request, 'core/index.html')



