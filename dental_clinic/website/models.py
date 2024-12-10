from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# # USER ROLES
# USER_ROLES = [
#     ('Guest', 'Guest'),
#     ('Customer', 'Customer'),
#     ('Dentist', 'Dentist'),
#     ('ClinicOwner', 'ClinicOwner'),
#     ('Admin', 'Admin'),
# ]

# class User(AbstractUser):
#     """
#     Custom User model to handle different roles.
#     """
#     role = models.CharField(max_length=20, choices=USER_ROLES)
#     address = models.TextField()
#     gender = models.TextField()
#     phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
#     is_verified = models.BooleanField(default=False)
#     image = models.ImageField(upload_to='specialties/', null=True, blank=True)  # Ảnh đại diện

#     def __str__(self):
#         return self.username

# class Clinic(models.Model):
#     """
#     Clinic model to store information about the dental clinics.
#     """
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_clinics")
#     clinic_name = models.CharField(max_length=100)
#     address = models.TextField()
#     description = models.TextField()
#     phone_number = models.CharField(max_length=15, unique=True)
#     opening_hours = models.CharField(max_length=50)
#     max_patients_per_slot = models.PositiveIntegerField()
#     max_treatment_per_slot = models.PositiveIntegerField()
#     slot_duration_minutes = models.PositiveIntegerField(default=45)
#     is_approved = models.BooleanField(default=False)
#     image = models.ImageField(upload_to='specialties/', null=True, blank=True)  # Ảnh đại diện

#     def __str__(self):
#         return self.clinic_name

# class Dentist(models.Model):
#     """
#     Dentist model to represent doctors in the system.
#     """
#     dentist = models.OneToOneField(User, on_delete=models.CASCADE, related_name="dentist_profile")
#     clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="dentists")
#     specialization = models.CharField(max_length=100)
#     experience_years = models.PositiveIntegerField()
#     description = models.TextField()

#     def __str__(self):
#         return self.dentist    
    
# class Specialty(models.Model):
#     """
#     Specialty model to represent specialties in the system.
#     """
#     id = models.AutoField(primary_key=True)  # ID tự động tăng
#     name = models.CharField(max_length=100, unique=True)  # Tên chuyên khoa
#     description = models.TextField(null=True, blank=True)  # Mô tả chuyên khoa
#     image = models.ImageField(upload_to='specialties/', null=True, blank=True)  # Ảnh đại diện

#     def __str__(self):
#         return self.name


# class Schedule(models.Model):
#     """
#     Schedule model to store working schedules for clinics and dentists.
#     """
#     clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="schedules")
#     dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE, related_name="schedules", null=True, blank=True)
#     day_of_week = models.CharField(
#         max_length=20,
#         choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
#                  ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')],
#     )
#     time = models.TextField()

#     def __str__(self):
#         return f"{self.clinic.clinic_name} - {self.day_of_week}"

# class Service(models.Model):
#     """
#     Service model for clinic services.
#     """
#     clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="services")
#     service_name = models.CharField(max_length=100)
#     description = models.TextField(null=True, blank=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.service_name} - {self.clinic.clinic_name}"
    
# class Appointment(models.Model):
#     """
#     Appointment model to manage appointments for customers.
#     """
#     STATUS_CHOICES = [
#         ('Scheduled', 'Scheduled'),
#         ('Completed', 'Completed'),
#         ('Cancelled', 'Cancelled'),
#     ]

#     customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
#     dentist = models.ForeignKey(Dentist, on_delete=models.SET_NULL, null=True, blank=True, related_name="appointments")
#     clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="appointments")
#     appointment_date = models.DateTimeField()
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
#     notes = models.TextField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Appointment  - {self.customer.username}"