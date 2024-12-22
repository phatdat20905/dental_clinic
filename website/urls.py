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
    # path("appointments/create/", views.create_appointment, name="create_appointment"),
    path("book-appointment/", views.book_appointment, name="book_appointment"),
    path("apppointment-access/", views.appointment_access, name="appointment_access"),

    path('search/', views.searchPage, name="search")
    # path('appointments/<int:clinic_id>/', views.appointment_form, name='appointment_form'),
]