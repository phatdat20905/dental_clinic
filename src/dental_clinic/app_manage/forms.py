from django import forms
from website.models import *
from tinymce.widgets import TinyMCE
from django.contrib.auth.forms import UserCreationForm
class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['dentist_notes', 'diagnosis', 'treatment_plan', 'medication', 'follow_up_date', 'image']  # Thêm 'follow_up_date'
        widgets = {
            'dentist_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'treatment_plan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'medication': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'follow_up_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # Widget cho trường ngày
        }
        labels = {
            'dentist_notes': 'Ghi chú của nha sĩ',
            'diagnosis': 'Chẩn đoán',
            'treatment_plan': 'Kế hoạch điều trị',
            'medication': 'Thuốc kê đơn',
            'follow_up_date': 'Ngày tái khám',
            'image': 'Hình ảnh (nếu có)',
        }

class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = [
            'clinic_name',
            'address',
            'description',
            'phone_number',
            'opening_hours',
            'max_patients_per_slot',
            'max_treatment_per_slot',
            'slot_duration_minutes',
            'image',
        ]
        widgets = {
            'description': TinyMCE(attrs={'cols': 80, 'rows': 20}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }


class DentistForm(forms.ModelForm):
    class Meta:
        model = Dentist
        fields = ['specialization', 'position', 'experience_years', 'description']
        widgets = {
            'description': TinyMCE(attrs={'cols': 80, 'rows': 20}),
        }

# class UserForm(forms.ModelForm):
#     password1 = forms.CharField(
#         widget=forms.PasswordInput(attrs={'placeholder': 'Nhập mật khẩu'}),
#         label="Mật khẩu",
#         max_length=128
#     )
#     password2 = forms.CharField(
#         widget=forms.PasswordInput(attrs={'placeholder': 'Xác nhận mật khẩu'}),
#         label="Xác nhận mật khẩu",
#         max_length=128
#     )
    
#     class Meta:
#         model = User
#         fields = ['email', 'full_name', 'gender', 'phone_number','address', 'image']
#         widgets = {
#             'address': forms.Textarea(attrs={'rows': 2}),
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         password1 = cleaned_data.get("password1")
#         password2 = cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Mật khẩu không khớp.")
        # return cleaned_data

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','full_name', 'gender', 'phone_number', 'address', 'image', 'password1', 'password2']


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'gender', 'phone_number', 'address', 'image']

class ScheduleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        clinic = kwargs.pop('clinic', None)
        super(ScheduleForm, self).__init__(*args, **kwargs)
        if clinic:
            self.fields['dentist'].queryset = Dentist.objects.filter(clinic=clinic)

    class Meta:
        model = Schedule
        fields = ['day', 'time', 'dentist']
        widgets = {
            'day': forms.DateInput(attrs={'type': 'date'}),  # Widget cho trường ngày
        }