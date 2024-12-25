from django.db import models
from django.contrib.auth.models import AbstractUser
from tinymce.models import HTMLField
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from .managers import CustomUserManager

class User(AbstractUser):
    # USER ROLES
    USER_ROLES = [
        ('Customer', 'Customer'),
        ('Dentist', 'Dentist'),
        ('ClinicOwner', 'ClinicOwner'),
        ('Admin', 'Admin'),
    ]
    USER_GENDERS = [
        ('Nam', 'Nam'),
        ('Nữ', 'Nữ')
    ]

    """
    Custom User model to handle different roles.
    """
    username = first_name = last_name = None
    email = models.EmailField(_("email address"), unique=True)
    full_name = models.CharField(max_length=120, null=True, blank=True)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='Customer')
    address = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=USER_GENDERS, default='Nam')
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='website/img/dentist', null=True, blank=True)  # Ảnh đại diện

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.full_name or 'Unnamed User'
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url
class Clinic(models.Model):
    """
    Clinic model to store information about the dental clinics.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_clinics")
    clinic_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    description = HTMLField()
    phone_number = models.CharField(max_length=15, unique=True)
    opening_hours = models.CharField(max_length=50)
    max_patients_per_slot = models.PositiveIntegerField()
    max_treatment_per_slot = models.PositiveIntegerField()
    slot_duration_minutes = models.PositiveIntegerField(default=45)
    is_approved = models.BooleanField(default=False)
    image = models.ImageField(upload_to='website/img/clinic', null=True, blank=True)

    def __str__(self):
        return self.clinic_name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.clinic_name)
        super().save(*args, **kwargs)
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

class Specialty(models.Model):
    """
    Specialty model to represent specialties in the system.
    """
    name = models.CharField(max_length=100, unique=True)  # Tên chuyên khoa
    description = HTMLField()  # Mô tả chuyên khoa
    image = models.ImageField(upload_to='website/img/specialties', null=True, blank=True)  # Ảnh đại diện

    def __str__(self):
        return self.name

class Dentist(models.Model):
    """
    Dentist model to represent doctors in the system.
    """
    POSITION_CHOICE = [
        ('Thạc sĩ', 'Thạc sĩ'),
        ('Tiến sĩ', 'Tiến sĩ'),
    ]

    dentist = models.OneToOneField(User, on_delete=models.CASCADE, related_name="dentist_profile")
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="dentists")
    specialization = models.CharField(max_length=30, null=True, blank=True)
    position = models.CharField(max_length=20, null=True, blank=True, choices=POSITION_CHOICE, default='Thạc sĩ')
    experience_years = models.PositiveIntegerField(null=True, blank=True)
    description = HTMLField()
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def __str__(self):
        return self.dentist.full_name or 'Unnamed Dentist'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.position}-{self.dentist.full_name}')
        super().save(*args, **kwargs)
    @property
    def ImageURL(self):
        try:
            url = self.dentist.image.url
        except:
            url = ""
        return url

class Schedule(models.Model):
    """
    Schedule model to store working schedules for clinics and dentists.
    """
    TIME_SLOTS = [
        ('08:00-08:45', '08:00 - 08:45'),
        ('09:00-09:45', '09:00 - 09:45'),
        ('10:00-10:45', '10:00 - 10:45'),
        ('11:00-11:45', '11:00 - 11:45'),
        ('13:00-13:45', '13:00 - 13:45'),
        ('14:00-14:45', '14:00 - 14:45'),
        ('15:00-15:45', '15:00 - 15:45'),
        ('16:00-16:45', '16:00 - 16:45'),
        ('17:00-17:45', '17:00 - 17:45'),
        ('18:00-18:45', '18:00 - 18:45'),
    ]

    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="schedules")
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE, related_name="schedules", null=True, blank=True)
    day = models.DateField(null=True, blank=True)
    time = models.CharField(max_length=20, choices=TIME_SLOTS, null=True, blank=True)

    def __str__(self):
        return f"{self.clinic.clinic_name} - {self.day}"

class Service(models.Model):
    """
    Service model for clinic services.
    """
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="services")
    service_name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20, null=True, blank=True)
    price = models.CharField(max_length=30, null=True, blank=True)
  
    def __str__(self):
        return f"{self.service_name}"

class Appointment(models.Model):
    """
    Appointment model to manage appointments for customers.
    """
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    dentist = models.ForeignKey(Dentist, on_delete=models.SET_NULL, null=True, blank=True, related_name="appointments")
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="appointments")
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name="appointments")
    appointment_date = models.DateField()
    time = models.CharField(max_length=20,null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment - {self.customer.full_name or 'Unnamed Customer'}"
