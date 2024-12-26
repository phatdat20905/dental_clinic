from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth

urlpatterns = [
    path('', views.homePage, name="home"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutPage, name ='logout'),
    path('clinic/<slug:slug>/', views.clinicPage, name="clinic"),
    path('api/get-available-times', views.get_available_times, name='get_available_times'),
    
    path("book-appointment/", views.book_appointment, name="book_appointment"),
    path("apppointment-access/", views.appointment_access, name="appointment_access"),

    path('search/', views.searchPage, name="search"),
    path('appointments/<slug:slug>/', views.appointment, name='appointments'),
    path('appointments/cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('profile/<slug:slug>/', views.profilePage, name="profile"),
    path("update-user/<slug:slug>/", views.update_user, name="update_user"),

    path('test/', views.testPage, name="test"),
]