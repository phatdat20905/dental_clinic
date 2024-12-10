from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def homePage(request):
    return render(request, 'website/home.html')

def loginPage(request):
    return render(request, 'website/login.html')