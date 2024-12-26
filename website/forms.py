from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','full_name', 'gender', 'phone_number', 'address', 'password1', 'password2']
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['clinic', 'dentist', 'appointment_date', 'time', 'status']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.Select(choices=Schedule.TIME_SLOTS),
        }
