from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.template import loader

# Create your views here.
def homePage(request):
    clinic = Clinic.objects.all()
    # template = loader.get_template('home.html')
    context = {
        'clinic': clinic,
    }
    return render(request, 'website/home.html', context)

def loginPage(request):
    return render(request, 'website/login.html')

def registerPage(request):
    form = UserCreationForm()
    context = {'form': form}
    return render(request, 'website/register.html', context)