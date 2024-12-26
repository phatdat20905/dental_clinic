from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth

urlpatterns = [
    path('', views.indexPage, name="index"),
    path('schedule/', views.schedulePage, name="schedule"),
    path('schedule/cancel/<int:schedule_id>/', views.cancel_schedule, name='cancel_schedule'),
    path('schedule/add/', views.add_schedule, name='add_schedule'),
]