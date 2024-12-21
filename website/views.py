from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
import json
from django.template import loader
from .forms import CreateUserForm

# Create your views here.
def homePage(request):
    clinic = Clinic.objects.all()
    dentist = Dentist.objects.all()
    # template = loader.get_template('home.html')
    context = {
        'clinic': clinic,
        'dentist': dentist,
    }
    return render(request, 'website/home.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            messages.error(request, "Can't Find User")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Wrong Email Or Password!")
    return render(request, 'website/login.html')

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}
    return render(request, 'website/register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def clinicPage(request):
    return render(request, 'website/clinic.html')