from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
import json
from django.template import loader
from .forms import CreateUserForm
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.
def homePage(request):
    clinic = Clinic.objects.all()
    dentist = Dentist.objects.all()
    # template = loader.get_template('home.html')
    context = {
        'clinic': clinic,
        'dentist': dentist,
    }
    return render(request, 'website/home.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            messages.error(request, "Can't Find User")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Wrong Email Or Password!")
    return render(request, 'website/login.html')

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}
    return render(request, 'website/register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def clinicPage(request, slug):
    clinic = Clinic.objects.get(slug=slug)
    dentists = Dentist.objects.filter(clinic=clinic)
    services = Service.objects.filter(clinic=clinic)
    schedules_by_dentist = {}
    for dentist in dentists:
        schedules = Schedule.objects.filter(clinic=clinic, dentist=dentist)
        schedules_by_dentist[dentist] = schedules
    context={
        "clinic": clinic,
        "dentists": dentists,
        "services": services,
        "schedules_by_dentist": schedules_by_dentist,
    }
    return render(request, 'website/clinic.html', context)

def get_available_times(request):
    """
    API để lấy danh sách các khung giờ của một bác sĩ trong ngày được chọn.
    """
    dentist_id = request.GET.get('dentist_id')
    selected_date = request.GET.get('date')

    # Kiểm tra tham số
    if not dentist_id or not selected_date:
        return JsonResponse({"error": "Missing parameters"}, status=400)

    try:
        # Kiểm tra dentist tồn tại
        dentist = Dentist.objects.get(id=dentist_id)
        date = parse_date(selected_date)

        if not date:
            return JsonResponse({"error": "Invalid date format"}, status=400)

        # Lọc danh sách lịch làm việc theo dentist và ngày
        schedules = Schedule.objects.filter(dentist=dentist, day=date)

        # Lấy danh sách khung giờ
        times = [schedule.time for schedule in schedules]

        return JsonResponse({"times": times}, status=200)

    except Dentist.DoesNotExist:
        return JsonResponse({"error": "Dentist not found"}, status=404)
    



# @login_required
# def create_appointment(request):
    if request.method == "POST":
        clinic_id = request.POST.get("clinic")
        dentist_id = request.POST.get("dentist")
        service_name = request.POST.get("service")
        appointment_date = request.POST.get("date")
        time_slot = request.POST.get("time")
        customer = request.user
        notes = request.POST.get("notes", "")

        # Validate and get objects
        clinic = get_object_or_404(Clinic, id=clinic_id)
        dentist = get_object_or_404(Dentist, id=dentist_id)
        service = get_object_or_404(Service, service_name=service_name, clinic=clinic)

        # Check if the time slot is available
        if Appointment.objects.filter(
            clinic=clinic,
            dentist=dentist,
            appointment_date=appointment_date,
            time=time_slot,
            status="Pending",
        ).exists():
            return JsonResponse({"error": "Time slot is already booked"}, status=400)

        # Create the appointment
        appointment = Appointment.objects.create(
            customer=customer,
            clinic=clinic,
            dentist=dentist,
            appointment_date=appointment_date,
            time=time_slot,
            notes=notes,
        )

        return JsonResponse({"message": "Appointment created successfully", "appointment_id": appointment.id})

    # Load the form with data for GET request
    clinics = Clinic.objects.all()
    dentists = Dentist.objects.all()
    services = Service.objects.all()
    return render(
        request,
        "appointments/create_appointment.html",
        {"clinics": clinics, "dentists": dentists, "services": services},
    )

# def get_available_times(request):
    dentist_id = request.GET.get("dentist_id")
    appointment_date = request.GET.get("date")

    if not dentist_id or not appointment_date:
        return JsonResponse({"error": "Dentist ID and date are required"}, status=400)

    schedules = Schedule.objects.filter(dentist_id=dentist_id, day=appointment_date)
    booked_times = Appointment.objects.filter(
        dentist_id=dentist_id,
        appointment_date=appointment_date,
        status="Pending"
    ).values_list("time", flat=True)

    available_times = [
        schedule.time
        for schedule in schedules
        if schedule.time not in booked_times
    ]

    return JsonResponse({"times": available_times})


def book_appointment(request):
    if request.method == "POST":
        clinic_id = request.POST.get("clinic")
        dentist_id = request.POST.get("dentist")
        service_name = request.POST.get("service")
        appointment_date = request.POST.get("date")
        time = request.POST.get("time")
        customer_name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        print('data', clinic_id, service_name, appointment_date, time, customer_name, phone, address)
        try:
            clinic = Clinic.objects.get(id=clinic_id)
            dentist = Dentist.objects.get(id=dentist_id) if dentist_id else None
            customer = User.objects.filter(full_name=customer_name, phone_number=phone).first()

            # Tạo người dùng nếu chưa tồn tại
            if not customer:
                customer = User.objects.create(
                    full_name=customer_name,
                    phone_number=phone,
                    address=address,
                    role="Customer",
                )

            # Tạo lịch hẹn
            appointment = Appointment.objects.create(
                customer=customer,
                clinic=clinic,
                dentist=dentist,
                appointment_date=appointment_date,
                time=time,
            )
            messages.success(request, "Đặt lịch hẹn thành công!")
            return redirect("appointment_success")
        except Exception as e:
            messages.error(request, f"Đặt lịch hẹn thất bại: {e}")
            return redirect("book_appointment")
    else:
        # Render form đặt lịch
        clinics = Clinic.objects.all()
        dentists = Dentist.objects.all()
        services = Service.objects.all()
        return render(request, "book_appointment.html", {
            "clinics": clinics,
            "dentists": dentists,
            "services": services,
        })