from django.contrib import admin
from .models import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'role', 'address', 'gender', 'phone_number')
    search_fields = ('email', 'full_name')
    list_filter = ('role', 'gender')
    fieldsets = [
        (
            "Infor",
            {
                "fields": ['email', 'full_name', 'password','role', 'address', 'gender', 'phone_number', 'image'],
            },
        ),
    ]

class ClinicAdmin(admin.ModelAdmin):
    list_display = ('owner', 'clinic_name', 'address', 'phone_number', 'opening_hours', 'is_approved')
    search_fields = ('clinic_name', 'address')

class DentistAdmin(admin.ModelAdmin):
    list_display = ('dentist', 'clinic', 'specialization', 'position')
    # search_fields = ('dentist', 'posotion')


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('dentist', 'clinic')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'unit', 'price')
    search_fields = ('service_name', 'price')

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'dentist', 'clinic', 'service', 'appointment_date', 'time', 'status')

admin.site.register(User, UserAdmin)
admin.site.register(Clinic, ClinicAdmin)
admin.site.register(Dentist, DentistAdmin)
admin.site.register(Specialty)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Appointment, AppointmentAdmin)
