from django import forms
from website.models import MedicalRecord

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