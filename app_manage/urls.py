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

    path('profile/<slug:slug>/', views.profileDentist, name="profile_dentist"),
    path("update-user/<slug:slug>/", views.update_profile, name="update_dentist"),

    path('my-clinics/', views.my_clinics, name='my_clinics'),
    path("add_clinic/", views.add_clinic, name="add_clinic"),
    path('clinic/edit/<slug:slug>/', views.edit_clinic, name='edit_clinic'),


    path('clinic/<slug:slug>/dentists/', views.list_dentists, name='list_dentists'),
    path("edit-dentist/<slug:slug>/", views.update_profile, name="edit-dentist"),

    path('clinic/<slug:slug>/dentists/add/', views.add_dentist, name='add_dentist'),
    path('clinic/<slug:slug>/edit_dentist/<int:dentist_id>/', views.edit_dentist, name='edit_dentist'),
    path('clinic/<slug:slug>/delete_dentist/<int:dentist_id>/', views.delete_dentist, name='delete_dentist'),

    path('clinic/<slug:slug>/schedule/', views.clinic_schedule, name='clinic_schedule'),
    path('clinic/<slug:slug>/cancel_schedule/<int:schedule_id>/', views.cancel_schedule_clinic, name='cancel_schedule_clinic'),
    path('clinic/<slug:slug>/add_schedule/', views.add_schedule_clinic, name='add_schedule_clinic'),
]