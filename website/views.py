from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
import json
from django.template import loader
from .forms import CreateUserForm, AppointmentForm
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.
def homePage(request):
    clinic = Clinic.objects.all()
    dentist = Dentist.objects.all()
    categories = Category.objects.all()
    
    context = {
        'clinic': clinic,
        'dentist': dentist,
        'categories': categories,
    }
    return render(request, 'website/home.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        # Kiểm tra vai trò của người dùng đã đăng nhập
        if request.user.role == "Dentist" or request.user.role == "ClinicOwner":
            return redirect('index')  # Trang admin cho Dentist
        return redirect('home')  # Trang chính cho các vai trò khác

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Can't Find User")
            return render(request, 'website/login.html')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # Chuyển hướng dựa trên vai trò của người dùng
            if user.role == "Dentist":
                return redirect('index')  # Trang admin cho Dentist
            return redirect('home')  # Trang chính cho các vai trò khác
        else:
            messages.error(request, "Wrong Email Or Password!")
    return render(request, 'website/login.html')

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # Lưu thông tin người dùng
            user = form.save()
            
            # Gửi email xác nhận
            email_subject = "Chào mừng bạn đến với nền tảng đặt lịch khám của chúng tôi!"
            email_message = (
                f"Xin chào {user.full_name},\n\n"
                f"Cảm ơn bạn đã đăng ký tài khoản tại hệ thống của chúng tôi.\n"
                f"Nếu bạn có bất kỳ thắc mắc nào, vui lòng liên hệ với chúng tôi qua {settings.EMAIL_HOST_USER} này.\n\n"
                f"Trân trọng,\n"
                f"Đội ngũ hỗ trợ khách hàng."
            )
            try:
                send_mail(
                    email_subject,
                    email_message,
                    settings.EMAIL_HOST_USER,
                    [user.email],  # Email người dùng
                    fail_silently=False,
                )
                messages.success(request, "Account created successfully! An email has been sent to your email address.")
            except Exception as e:
                messages.warning(request, f"Account created successfully, but email sending failed: {e}")

            return redirect('login')

    context = {'form': form}
    return render(request, 'website/register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def clinicPage(request, slug):
    customer = request.user
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
        "customer": customer,
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

@login_required(login_url='register')  # Chuyển hướng đến trang đăng ký nếu chưa đăng nhập
def book_appointment(request):
    print(f"Request method: {request.method}")
    if request.method == "POST":
        clinic_id = request.POST.get("clinic")
        dentist_id = request.POST.get("dentist")
        service_id = request.POST.get("service")
        appointment_date = request.POST.get("date")
        time = request.POST.get("time")
        customer_name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        print(f"clinic_id: {clinic_id}, dentist_id: {dentist_id}, service_id: {service_id}")
        print(f"appointment_date: {appointment_date}, time: {time}")
        print(f"customer_name: {customer_name}, phone: {phone}, address: {address}")

        try:
            # Kiểm tra dữ liệu nhập vào
            if not clinic_id or not service_id or not appointment_date or not time or not customer_name or not phone:
                raise ValueError("Vui lòng điền đầy đủ thông tin.")

            clinic = Clinic.objects.get(id=clinic_id)
            print('Clinic', clinic)

            dentist = Dentist.objects.get(id=dentist_id) if dentist_id else None
            print('dentist', dentist)

            service = Service.objects.get(id=service_id)

            # Lấy thông tin khách hàng từ người dùng đang đăng nhập
            customer = request.user
            # # Tìm hoặc tạo khách hàng
            # customer, created = User.objects.get_or_create(
            #     full_name=customer_name,
            #     phone_number=phone,
            #     defaults={"address": address, "role": "Customer"}
            # )

            # Kiểm tra nếu khách hàng đã có lịch hẹn
            if Appointment.objects.filter(customer=customer).exists():
                raise ValueError("Khách hàng này đã có lịch hẹn. Vui lòng hủy lịch hẹn trước đó để đặt lịch mới.")

            # Kiểm tra xem đã có lịch hẹn trùng không
            if Appointment.objects.filter(
                clinic=clinic,
                dentist=dentist,
                appointment_date=appointment_date,
                time=time
            ).exists():
                raise ValueError("Lịch hẹn này đã được đặt, vui lòng chọn thời gian khác.")

            # Tạo lịch hẹn
            Appointment.objects.create(
                customer=customer,
                clinic=clinic,
                dentist=dentist,
                service=service,
                full_name=customer_name,
                phone_number=phone,
                address=address,
                appointment_date=appointment_date,
                time=time,
            )

            # Gửi email xác nhận
            email_subject = "Xác nhận lịch hẹn nha khoa"
            email_message = (
                f"Xin chào {customer_name},\n\n"
                f"Cảm ơn bạn đã đặt lịch hẹn tại {clinic.clinic_name}.\n"
                f"Thông tin lịch hẹn của bạn:\n"
                f"- Ngày: {appointment_date}\n"
                f"- Giờ: {time}\n"
                f"- Nha sĩ: {dentist}\n"
                f"- Dịch vụ: {service.service_name}\n"
                f"- Địa chỉ phòng khám: {clinic.address}\n\n"
                f"Vui lòng liên hệ số điện thoại: {clinic.phone_number} hoặc email: {settings.EMAIL_HOST_USER} nếu bạn cần hỗ trợ thêm.\n"
                f"Trân trọng,\n{clinic.clinic_name}"
            )
            send_mail(
                email_subject,
                email_message,
                settings.EMAIL_HOST_USER,
                [customer.email],
                # ['ngophatdat80@gmail.com'],  # Địa chỉ email của khách hàng
                fail_silently=False,
            )

            messages.success(request, "Đặt lịch hẹn thành công!")
            return redirect("appointment_access")
        except Clinic.DoesNotExist:
            messages.error(request, "Phòng khám không tồn tại.")
        except Dentist.DoesNotExist:
            messages.error(request, "Bác sĩ không tồn tại.")
        except Service.DoesNotExist:
            messages.error(request, "Dịch vụ không tồn tại.")
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"Có lỗi xảy ra: {e}")

        return redirect("home")

    else:
        clinics = Clinic.objects.all()
        dentists = Dentist.objects.all()
        services = Service.objects.all()
        return render(request, "book_appointment.html", {
            "clinics": clinics,
            "dentists": dentists,
            "services": services,
        })

def appointment_access(request):
    return render(request, "website/appointment_access.html")


def searchPage(request):
    if request.method == "POST":
        search = request.POST.get("searched", "").strip()  # Lấy từ khóa tìm kiếm và loại bỏ khoảng trắng thừa
        
        # Tìm kiếm phòng khám (không phân biệt hoa thường)
        clinic_results = Clinic.objects.filter(clinic_name__icontains=search)
        
        # Tìm kiếm nha sĩ (không phân biệt hoa thường)
        dentist_results = User.objects.filter(full_name__icontains=search, role="Dentist")
        
        # Lấy thông tin từ Dentist model (nếu có)
        dentist_ids = dentist_results.values_list('id', flat=True)  # Lấy danh sách ID của nha sĩ
        dentist_details = Dentist.objects.filter(id__in=dentist_ids)  # Lấy thông tin từ bảng Dentist
        
        print('Dentist IDs:', list(dentist_ids))  # Debug: In ra danh sách ID của nha sĩ
        print('Dentist Details:', dentist_details)  # Debug: In ra thông tin chi tiết nha sĩ
        
        context = {
            "search": search,
            "clinic": clinic_results,
            "dentist": dentist_details,  # Trả về thông tin chi tiết từ bảng Dentist
        }
        return render(request, "website/search.html", context)
    
    # Trường hợp không có POST request
    return render(request, "website/search.html", {"search": None})


def appointment(request, slug):
    try:
        # Lấy thông tin khách hàng
        customer = get_object_or_404(User, slug=slug)
        
        # Lấy danh sách lịch hẹn của khách hàng
        appointments = Appointment.objects.filter(customer=customer)

        context = {
            "customer": customer,
            "appointments": appointments,
        }
        return render(request, "website/appointment_table.html", context)
    except Exception as e:
        return render(request, "website/appointment_table.html", {"error": str(e)})
    
def cancel_appointment(request, appointment_id):
    try:
        # Lấy lịch hẹn theo ID
        appointment = get_object_or_404(Appointment, id=appointment_id)

        # Kiểm tra trạng thái lịch hẹn
        if appointment.status == "Xác nhận":
            messages.error(request, "Lịch hẹn đã được xác nhận và không thể hủy.")
        else:
            # Xóa lịch hẹn nếu chưa xác nhận
            appointment.delete()
            # messages.success(request, "Lịch hẹn đã được hủy thành công!")
    except Exception as e:
        messages.error(request, f"Có lỗi xảy ra khi hủy lịch hẹn: {e}")

    # Quay lại trang danh sách lịch hẹn
    return redirect('appointments', slug=request.user.slug)
def profilePage(request, slug):
    # Lấy thông tin khách hàng
    customer = get_object_or_404(User, slug=slug)
    context = {
            "customer": customer,
        }
    return render(request, "website/profile.html", context)

def update_user(request, slug):
    user = get_object_or_404(User, slug=slug)

    if request.method == "POST":
        email = request.POST.get("email")
        full_name = request.POST.get("fullname")
        gender = request.POST.get("gender")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        image = request.FILES.get("image")

        try:
            user.email = email
            user.full_name = full_name
            user.gender = gender
            user.phone_number = phone
            user.address = address

            if image:
                user.image = image

            user.save()
            messages.success(request, "Cập nhật thông tin người dùng thành công!")
            return redirect("profile", slug=slug)  # Cung cấp customer_id
        except Exception as e:
            messages.error(request, f"Có lỗi xảy ra: {e}")

    context = {"user": user}
    return render(request, context)

def medical_records(request, slug):
    # Lấy thông tin khách hàng
    customer = get_object_or_404(User, slug=slug)
    
    # Lấy danh sách lịch hẹn đã hoàn thành của khách hàng
    completed_appointments = Appointment.objects.filter(customer=customer, status="Hoàn thành")

    # Lấy danh sách kết quả khám tương ứng
    medical_record = MedicalRecord.objects.get(appointment__in=completed_appointments)
    # Truyền dữ liệu vào context
    context = {
        'customer': customer,
        'medical_record': medical_record,
    }
    
    return render(request, 'website/medical_record_detail.html', context)



def testPage(request):
    return render(request, "website/test.html")



def categories(request, slug):
    selected_category = get_object_or_404(Category, slug=slug)
    service_items = ServiceItem.objects.filter(category=selected_category)
    context = {
        'selected_category': selected_category,
        'service_items': service_items,
    }
    return render(request, 'website/services.html', context)




