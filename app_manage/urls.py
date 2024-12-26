from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth

urlpatterns = [
    path('', views.indexPage, name="index"),
    path('schedule/', views.schedulePage, name="schedule"),
    path('schedule/cancel/<int:schedule_id>/', views.cancel_schedule, name='cancel_schedule'),
    path('schedule/add/', views.add_schedule, name='add_schedule'),
    path('appointment_schedule/', views.appointment_schedule, name="appointment_schedule"),
    path('appointment_schedule/update/<int:appointment_id>/', views.update_appointments, name="update_appointments"),
    path('add_medical_record/<int:appointment_id>/', views.add_medical_record, name='add_medical_record'),
]