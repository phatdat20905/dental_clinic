from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from django.core.exceptions import ValidationError

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



class DentistAdminForm(forms.ModelForm):
    class Meta:
        model = Dentist
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dentist'].queryset = User.objects.filter(role='Dentist')

class ClinicAdminForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].queryset = User.objects.filter(role='ClinicOwner')

   

