from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Clinic)
admin.site.register(Dentist)
admin.site.register(Specialty)
admin.site.register(Schedule)
admin.site.register(Service)
admin.site.register(Appointment)
