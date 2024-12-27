from django.shortcuts import render, redirect, get_object_or_404
from website.models import *
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from .forms import MedicalRecordForm
from datetime import datetime, timedelta

# Create your views here.
def indexPage(request):
    return render(request, 'app_manage/dashboard.html')


# @login_required(login_url='login')  # Đảm bảo chỉ nha sĩ đã đăng nhập mới có thể truy cập
# def schedulePage(request):
#     try:
#         # Lấy thông tin nha sĩ đang đăng nhập
#         user = request.user

#         # Kiểm tra xem người dùng hiện tại có phải là nha sĩ không
#         if not user.role == "Dentist":  # Giả định `role` xác định vai trò người dùng
#             raise ValueError("Bạn không có quyền truy cập vào trang này.")

#         dentist = Dentist.objects.get(dentist=user)
        
#         # Lấy lịch làm việc của nha sĩ
#         schedule = Schedule.objects.filter(dentist=dentist)

#         # Nếu không có lịch làm việc nào, tạo lịch làm việc mặc định
#         if not schedule.exists():
#             today = datetime.now().date()
#             time_slots = Schedule.TIME_SLOTS  # Các khung giờ mặc định từ model
#             default_clinic = Clinic.objects.first()  # Giả định sử dụng phòng khám đầu tiên
#             if not default_clinic:
#                 raise ValueError("Không có phòng khám nào để tạo lịch làm việc mặc định.")

#             # Tạo lịch cho 7 ngày tiếp theo
#             new_schedules = []
#             for i in range(7):  # Lặp qua 7 ngày tiếp theo
#                 day = today + timedelta(days=i + 1)  # Từ ngày mai trở đi
#                 for time_slot in time_slots:
#                     new_schedules.append(
#                         Schedule(
#                             clinic=default_clinic,
#                             dentist=dentist,
#                             day=day,
#                             time=time_slot[0],
#                         )
#                     )

#             # Lưu tất cả lịch làm việc mới
#             Schedule.objects.bulk_create(new_schedules)
#             messages.success(request, "Lịch làm việc mặc định đã được tạo thành công!")
#             schedule = Schedule.objects.filter(dentist=dentist)

#         context = {
#             'schedule': schedule,  # Truyền danh sách lịch làm việc vào context
#         }
#         return render(request, 'app_manage/schedule.html', context)

#     except ValueError as e:
#         messages.error(request, str(e))
#         return redirect('home')  # Chuyển hướng về trang chủ nếu có lỗi

#     except Exception as e:
#         messages.error(request, f"Có lỗi xảy ra: {e}")
#         return redirect('home')

@login_required(login_url='login')  # Đảm bảo chỉ nha sĩ đã đăng nhập mới có thể truy cập
def schedulePage(request):
    try:
        # Lấy thông tin nha sĩ đang đăng nhập
        user = request.user

        # Kiểm tra xem người dùng hiện tại có phải là nha sĩ không
        if not user.role == "Dentist":  # Giả định `role` xác định vai trò người dùng
            raise ValueError("Bạn không có quyền truy cập vào trang này.")

        dentist = Dentist.objects.get(dentist=user)
        
        # Lấy lịch làm việc của nha sĩ
        schedule = Schedule.objects.filter(dentist=dentist)

        # Nếu không có lịch làm việc nào, chuyển hướng tới trang thêm lịch
        if not schedule.exists():
            messages.info(request, "Hiện tại bạn chưa có lịch làm việc. Vui lòng thêm lịch làm việc.")
            return redirect('add_schedule')  # 'add_schedule' là tên URL của trang thêm lịch

        context = {
            'schedule': schedule,  # Truyền danh sách lịch làm việc vào context
        }
        return render(request, 'app_manage/schedule.html', context)

    except ValueError as e:
        messages.error(request, str(e))
        return redirect('home')  # Chuyển hướng về trang chủ nếu có lỗi

    except Exception as e:
        messages.error(request, f"Có lỗi xảy ra: {e}")
        return redirect('home')


def cancel_schedule(request, schedule_id):
    try:
        # Lấy lịch hẹn theo ID
        schedule = get_object_or_404(Schedule, id=schedule_id)
        schedule.delete()
        # Kiểm tra trạng thái lịch hẹn
        # if schedule.status == "Xác nhận":
        #     messages.error(request, "Lịch hẹn đã được xác nhận và không thể hủy.")
        # else:
        #     # Xóa lịch hẹn nếu chưa xác nhận
        #     schedule.delete()
        #     # messages.success(request, "Lịch hẹn đã được hủy thành công!")
    except Exception as e:
        messages.error(request, f"Có lỗi xảy ra khi hủy lịch hẹn: {e}")

    # Quay lại trang danh sách lịch hẹn
    return redirect('schedule')

@login_required(login_url='login')  # Chỉ cho phép người dùng đã đăng nhập
def add_schedule(request):
    try:
        # Lấy thông tin người dùng hiện tại
        user = request.user

        # Kiểm tra vai trò người dùng (chỉ cho phép Dentist thêm lịch)
        if not user.role == "Dentist":
            raise ValueError("Bạn không có quyền thêm lịch làm việc.")

        dentist = Dentist.objects.get(dentist=user)  # Lấy thông tin nha sĩ từ người dùng
        clinics = Clinic.objects.all()  # Lấy danh sách phòng khám để hiển thị trong form

        if request.method == "POST":
            # Lấy dữ liệu từ form
            clinic_id = request.POST.get("clinic")
            day = request.POST.get("day")
            time_slot = request.POST.get("time")

            # Kiểm tra dữ liệu
            if not clinic_id or not day or not time_slot:
                raise ValueError("Vui lòng nhập đầy đủ thông tin phòng khám, ngày và khung giờ.")

            clinic = Clinic.objects.get(id=clinic_id)

            # Kiểm tra lịch làm việc trùng lặp
            if Schedule.objects.filter(clinic=clinic, dentist=dentist, day=day, time=time_slot).exists():
                raise ValueError("Lịch làm việc đã tồn tại trong hệ thống.")

            # Thêm lịch làm việc mới
            Schedule.objects.create(
                clinic=clinic,
                dentist=dentist,
                day=day,
                time=time_slot
            )

            messages.success(request, "Thêm lịch làm việc thành công!")
            return redirect("schedule")  # Chuyển về trang danh sách lịch làm việc

        context = {
            "clinics": clinics,
            "time_slots": Schedule.TIME_SLOTS,
        }
        return render(request, "app_manage/add_schedule.html", context)

    except ValueError as e:
        messages.error(request, str(e))
        return redirect("schedule")

    except Exception as e:
        messages.error(request, f"Có lỗi xảy ra: {e}")
        return redirect("schedule")
    

def appointment_schedule(request):
    try:
        # Lấy thông tin nha sĩ đang đăng nhập
        user = request.user

        # Kiểm tra xem người dùng hiện tại có phải là nha sĩ không
        if not user.role == "Dentist":  # Giả định `role` xác định vai trò người dùng
            raise ValueError("Bạn không có quyền truy cập vào trang này.")

        dentist = Dentist.objects.get(dentist=user)
        
        # Lấy lịch làm việc của nha sĩ
        appointments = Appointment.objects.filter(dentist=dentist)

        # Nếu không có lịch làm việc nào, chuyển hướng tới trang thêm lịch
        if not appointments.exists():
            messages.info(request, "Hiện tại bạn chưa có lịch làm việc. Vui lòng thêm lịch làm việc.")
            return redirect('add_schedule')  # 'add_schedule' là tên URL của trang thêm lịch

        context = {
            'appointments': appointments,  # Truyền danh sách lịch làm việc vào context
        }
        return render(request, 'app_manage/appointment_schedule.html', context)

    except ValueError as e:
        messages.error(request, str(e))
        return redirect('home')  # Chuyển hướng về trang chủ nếu có lỗi

    except Exception as e:
        messages.error(request, f"Có lỗi xảy ra: {e}")
        return redirect('home')
    
def update_appointments(request, appointment_id):
    try:
        # Lấy lịch hẹn theo ID
        appointment = get_object_or_404(Appointment, id=appointment_id)
        # Kiểm tra trạng thái lịch hẹn
        if appointment.status == "Xác nhận":
            messages.error(request, "Lịch hẹn đã được xác nhận và không thể hủy.")
        else:
            # xác nhận lịch hẹn nếu chưa xác nhận
            appointment.status = "Xác nhận"
            appointment.save()
            messages.success(request, "Lịch h��n đã được xác nhận thành công!")
    except Exception as e:
        messages.error(request, f"Có lỗi xảy ra khi xác nhận lịch hẹn: {e}")

    # Quay lại trang danh sách lịch hẹn
    return redirect('appointment_schedule')
        
        
def add_medical_record(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Kiểm tra trạng thái cuộc hẹn
    if appointment.status == 'Hoàn thành':
        messages.error(request, "Chỉ có thể nhập kết quả cho cuộc hẹn đang chờ.")
        return redirect('appointment_schedule')

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES)
        if form.is_valid():
            # Lưu kết quả khám
            medical_record = form.save(commit=False)
            medical_record.appointment = appointment
            medical_record.save()

            # Cập nhật trạng thái cuộc hẹn
            appointment.status = 'Hoàn thành'
            appointment.save()

            messages.success(request, "Kết quả khám đã được lưu.")
            return redirect('appointment_schedule')
    else:
        form = MedicalRecordForm()

    return render(request, 'app_manage/add_medical_record.html', {'form': form, 'appointment': appointment})


def profileDentist(request, slug):
    # Lấy thông tin khách hàng
    dentist = get_object_or_404(User, slug=slug)
    context = {
            "dentist": dentist,
        }
    return render(request, "app_manage/profile_dentist.html", context)

def update_profile(request, slug):
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
            return redirect("profile_dentist", slug=slug)  # Cung cấp customer_id
        except Exception as e:
            messages.error(request, f"Có lỗi xảy ra: {e}")

    context = {"user": user}
    return render(request, 'app_manage/update_profile.html', context)