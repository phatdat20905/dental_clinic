from django.db import models
from django.contrib.auth.models import AbstractUser
from tinymce.models import HTMLField
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from .managers import CustomUserManager
from django.core.validators import RegexValidator

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
    phone_number = models.CharField(max_length=10,unique=True, blank=True, null=True, validators=[RegexValidator(
        regex=r"^\d{10}", message="Phone number must be 10 digits only.")])
    image = models.ImageField(upload_to='website/img/dentist', null=True, blank=True)  # Ảnh đại diện
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)


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
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name)
        super().save(*args, **kwargs)
class Clinic(models.Model):
    """
    Clinic model to store information about the dental clinics.
    """
    STATUS_CHOICES = [
        ('Chờ', 'Chờ'),
        ('Xác nhận', 'Xác nhận'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_clinics")
    clinic_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    description = HTMLField(null=True, blank=True)
    phone_number = models.CharField(max_length=10,unique=True, blank=True, null=True, validators=[RegexValidator(
        regex=r"^\d{10}", message="Phone number must be 10 digits only.")])
    opening_hours = models.CharField(max_length=50)
    max_patients_per_slot = models.PositiveIntegerField()
    max_treatment_per_slot = models.PositiveIntegerField()
    slot_duration_minutes = models.PositiveIntegerField(default=45)
    image = models.ImageField(upload_to='website/img/clinic', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Xác nhận', null=True, blank=True)

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

# class Specialty(models.Model):
#     """
#     Specialty model to represent specialties in the system.
#     """
#     name = models.CharField(max_length=100, unique=True)  # Tên chuyên khoa
#     description = HTMLField()  # Mô tả chuyên khoa
#     image = models.ImageField(upload_to='website/img/specialties', null=True, blank=True)  # Ảnh đại diện

#     def __str__(self):
#         return self.name

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
    description = HTMLField(null=True, blank=True)
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
        ('Chờ', 'Chờ'),
        ('Xác nhận', 'Xác nhận'),
        ('Hoàn thành', 'Hoàn thành'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    dentist = models.ForeignKey(Dentist, on_delete=models.SET_NULL, null=True, blank=True, related_name="appointments")
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="appointments")
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name="appointments")
    full_name = models.CharField(max_length=120, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    appointment_date = models.DateField()
    time = models.CharField(max_length=20,null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Chờ', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment - {self.customer.full_name or 'Unnamed Customer'}"

class MedicalRecord(models.Model):
    """
    MedicalRecord model to store examination results for customers.
    """
    appointment = models.OneToOneField(
        Appointment, on_delete=models.CASCADE, related_name="medical_record"
    )  # Mỗi cuộc hẹn có 1 kết quả khám
    dentist_notes = models.TextField(null=True, blank=True)  # Ghi chú của nha sĩ
    diagnosis = models.TextField(null=True, blank=True)  # Chẩn đoán
    treatment_plan = models.TextField(null=True, blank=True)  # Kế hoạch điều trị
    medication = models.TextField(null=True, blank=True)  # Thuốc kê đơn
    follow_up_date = models.DateField(null=True, blank=True)  # Ngày tái khám
    image = models.ImageField(upload_to='website/img/medical_records', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)  # Thời gian tạo
    updated_at = models.DateTimeField(auto_now=True)  # Thời gian cập nhật

    def __str__(self):
        return f"Medical Record - {self.appointment.customer.full_name or 'Unnamed Customer'}"


# class Notification(models.Model):
#     """
#     Notification model for reminders and updates.
#     """
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
#     message = models.TextField()  # Nội dung thông báo
#     is_read = models.BooleanField(default=False)  # Trạng thái đã đọc
#     created_at = models.DateTimeField(auto_now_add=True)  # Thời gian tạo
#     send_at = models.DateTimeField(null=True, blank=True)  # Thời gian gửi

#     def __str__(self):
#         return f"Notification for {self.user.full_name or 'Unnamed User'}"



class Category(models.Model):
    name = models.CharField(max_length=100)
    description = HTMLField(null=True, blank=True)
    image = models.ImageField(upload_to='website/img/service', null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class ServiceItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="service_items")
    service_name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20, null=True, blank=True)
    price = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.service_name
