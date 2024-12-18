from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth

urlpatterns = [
    path('', views.homePage, name="home"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutPage, name ='logout'),
]