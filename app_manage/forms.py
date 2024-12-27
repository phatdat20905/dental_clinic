from django import forms
from website.models import *
from tinymce.widgets import TinyMCE
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

# class DentistForm(forms.ModelForm):
#     specialization = forms.CharField(max_length=30, required=True)
#     position = forms.ChoiceField(choices=Dentist.POSITION_CHOICE, required=True)
#     experience_years = forms.IntegerField(required=True)
#     description = forms.CharField(widget=forms.Textarea, required=True)

#     class Meta:
#         model = User
#         fields = ['full_name', 'email', 'phone_number', 'image']