from django.contrib import admin
from .models import *
from .forms import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'role', 'address', 'gender', 'phone_number')
    search_fields = ('email', 'full_name')
    list_filter = ('role', 'gender')
    fieldsets = [
        (
            "Infor",
            {
                "fields": ['email', 'full_name', 'password','role', 'address', 'gender', 'phone_number', 'image', 'slug'],
            },
        ),
        (
            "Permissions",
            {
                "fields": ['is_staff', 'is_superuser', 'is_active'],
            },
        )
    ]
    

class ClinicAdmin(admin.ModelAdmin):
    list_display = ('owner', 'clinic_name', 'address', 'phone_number', 'opening_hours', 'status')
    search_fields = ('clinic_name', 'address')
    form = ClinicAdminForm

class DentistAdmin(admin.ModelAdmin):
    list_display = ('dentist', 'clinic', 'specialization', 'position')
    # search_fields = ('dentist', 'posotion')
    form = DentistAdminForm
    


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('dentist', 'clinic', 'day', 'time')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'unit', 'price', 'clinic')
    search_fields = ('service_name', 'price')

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'dentist', 'clinic', 'service', 'appointment_date', 'time', 'status')

class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ("appointment", "created_at", "updated_at")
    search_fields = ("appointment__customer__full_name", "diagnosis", "treatment_plan")
    list_filter = ("created_at",)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class ServiceItemAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'category', 'unit', 'price')
    search_fields = ('service_name', 'category__name')
    list_filter = ('category',)


admin.site.register(User, UserAdmin)
admin.site.register(Clinic, ClinicAdmin)
admin.site.register(Dentist, DentistAdmin)
# admin.site.register(Specialty)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(MedicalRecord, MedicalRecordAdmin)
# admin.site.register(Notification)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ServiceItem, ServiceItemAdmin)