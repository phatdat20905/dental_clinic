from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from website.models import *
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from .forms import *
from django.utils.text import slugify
from datetime import datetime, timedelta
from .searchs import search_all
# Create your views here.
def indexPage(request):
    if request.user.role == 'Customer':
        return render(request, '403.html', {"message": "You are not authorized to view this page."})

    clinics = Clinic.objects.filter(owner=request.user)
    context = {
        'clinics': clinics,
    }
    return render(request, 'app_manage/home.html', context)

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
            'dentist': dentist,
            'schedule': schedule,  # Truyền danh sách lịch làm việc vào context
        }
        return render(request, 'app_manage/dentist/schedule.html', context)

    except ValueError as e:
        messages.error(request, str(e))
        # return redirect('home')  # Chuyển hướng về trang chủ nếu có lỗi

    # except Exception as e:
    #     messages.error(request, f"Có lỗi xảy ra: {e}")
    #     # return redirect('home')

@login_required
def cancel_schedule(request, schedule_id):
    try:
        # Lấy lịch hẹn theo ID
        schedule = get_object_or_404(Schedule, id=schedule_id)
        schedule.delete()
        # # Kiểm tra trạng thái lịch hẹn
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
        clinics = Clinic.objects.filter(dentists=dentist)  # Lấy danh sách phòng khám để hiển thị trong form

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
        return render(request, "app_manage/dentist/add_schedule.html", context)

    except ValueError as e:
        messages.error(request, str(e))
        return redirect("schedule")

    except Exception as e:
        messages.error(request, f"Có lỗi xảy ra: {e}")
        return redirect("schedule")
    
@login_required
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

        # # Nếu không có lịch làm việc nào, chuyển hướng tới trang thêm lịch
        # if not appointments.exists():
        #     messages.info(request, "Hiện tại bạn chưa có lịch làm việc. Vui lòng thêm lịch làm việc.")
        #     return redirect('add_schedule')  # 'add_schedule' là tên URL của trang thêm lịch

        context = {
            'appointments': appointments,  # Truyền danh sách lịch làm việc vào context
        }
        return render(request, 'app_manage/dentist/appointment_schedule.html', context)

    except ValueError as e:
        messages.error(request, str(e))
        return redirect('home')  # Chuyển hướng về trang chủ nếu có lỗi

    except Exception as e:
        messages.error(request, f"Có lỗi xảy ra: {e}")
        return redirect('home')

@login_required
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
        
@login_required
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

    return render(request, 'app_manage/dentist/add_medical_record.html', {'form': form, 'appointment': appointment})

@login_required
def profileDentist(request, slug):
    # Lấy thông tin khách hàng
    dentist = get_object_or_404(User, slug=slug)
    context = {
            "dentist": dentist,
        }
    return render(request, "app_manage/dentist/profile_dentist.html", context)
@login_required
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
    return render(request, 'app_manage/dentist/update_profile.html', context)

@login_required
def my_clinics(request):
    if request.user.role != 'ClinicOwner':
        return render(request, '403.html', {"message": "You are not authorized to view this page."})

    clinics = Clinic.objects.filter(owner=request.user, status = "Xác nhận")
    context = {
        'clinics': clinics,
    }
    return render(request, 'app_manage/clinic/my_clinics.html', context)
@login_required
def add_clinic(request):
    if request.method == "POST":
        clinic_name = request.POST.get("clinic_name")
        address = request.POST.get("address")
        description = request.POST.get("description")
        phone_number = request.POST.get("phone_number")
        opening_hours = request.POST.get("opening_hours")
        max_patients_per_slot = request.POST.get("max_patients_per_slot")
        max_treatment_per_slot = request.POST.get("max_treatment_per_slot")
        slot_duration_minutes = request.POST.get("slot_duration_minutes")
        image = request.FILES.get("image")
        # owner_id = request.POST.get(id=request.user.id)

        try:
            # owner = User.objects.get(id=owner_id, role="ClinicOwner")
            owner = request.user
            clinic = Clinic.objects.create(
                owner=owner,
                clinic_name=clinic_name,
                address=address,
                description=description,
                phone_number=phone_number,
                opening_hours=opening_hours,
                max_patients_per_slot=max_patients_per_slot,
                max_treatment_per_slot=max_treatment_per_slot,
                slot_duration_minutes=slot_duration_minutes,
                image=image,
            )
            clinic.save()
            messages.success(request, "Clinic added successfully!")
            return redirect("clinic_list")
        except User.DoesNotExist:
            messages.error(request, "Invalid clinic owner.")
        except Exception as e:
            messages.error(request, f"Error: {e}")
    return render(request, "app_manage/clinic/add_clinic.html")

@login_required
def edit_clinic(request, slug):
    # Lấy phòng khám dựa trên slug
    clinic = get_object_or_404(Clinic, slug=slug)

    # Kiểm tra quyền sở hữu
    if clinic.owner != request.user:
        return render(request, '403.html', {"message": "You are not authorized to edit this clinic."})

    # Nếu là POST, xử lý form
    if request.method == 'POST':
        form = ClinicForm(request.POST, request.FILES, instance=clinic)
        if form.is_valid():
            form.save()
            return redirect('my_clinics')  # Chuyển hướng về danh sách phòng khám
    else:
        form = ClinicForm(instance=clinic)

    # Hiển thị form chỉnh sửa
    context = {
        'form': form,
        'clinic': clinic,
    }
    return render(request, 'app_manage/clinic/edit_clinic.html', context)

@login_required
def list_dentists(request, slug):
    # Lấy phòng khám dựa trên slug và chủ sở hữu
    clinic = get_object_or_404(Clinic, slug=slug, owner=request.user)

    # Lấy danh sách nha sĩ thuộc phòng khám
    dentists = Dentist.objects.filter(clinic=clinic)

    # Nếu không có nha sĩ, thêm thông báo
    if not dentists.exists():
        messages.info(request, "Phòng khám hiện chưa có nha sĩ nào. Hãy thêm nha sĩ mới!")

    return render(request, 'app_manage/dentist/dentist_list.html', {'clinic': clinic, 'dentists': dentists})


@login_required
def add_dentist(request, slug):
    clinic = get_object_or_404(Clinic, slug=slug, owner=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES)
        dentist_form = DentistForm(request.POST)
        if user_form.is_valid() and dentist_form.is_valid():
            # Tạo tài khoản User cho nha sĩ
            user = user_form.save(commit=False)
            user.role = 'Dentist'
            # user.set_password(user_form.cleaned_data['password1'])  # Lấy mật khẩu từ password1
            user.save()

            # Liên kết thông tin Dentist
            dentist = dentist_form.save(commit=False)
            dentist.dentist = user
            dentist.clinic = clinic
            dentist.save()

            messages.success(request, "Nha sĩ đã được thêm thành công!")
            return redirect('add_dentist', slug=slug)
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin.")
    else:
        user_form = UserForm()
        dentist_form = DentistForm()

    context = {
        'user_form': user_form,
        'dentist_form': dentist_form,
    }
    return render(request, 'app_manage/dentist/add_dentist.html', context)

@login_required
def edit_dentist(request, slug, dentist_id):
    clinic = get_object_or_404(Clinic, slug=slug, owner=request.user)
    dentist = get_object_or_404(Dentist, id=dentist_id, clinic=clinic)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, request.FILES, instance=dentist.dentist)
        dentist_form = DentistForm(request.POST, instance=dentist)
        if user_form.is_valid() and dentist_form.is_valid():
            user_form.save()
            dentist_form.save()
            messages.success(request, "Thông tin nha sĩ đã được cập nhật thành công!")
            return redirect('list_dentists', slug=slug)
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin.")
            print(user_form.errors, dentist_form.errors)
    else:
        user_form = UpdateUserForm(instance=dentist.dentist)
        dentist_form = DentistForm(instance=dentist)

    context = {
        'user_form': user_form,
        'dentist_form': dentist_form,
        'clinic': clinic,
    }
    return render(request, 'app_manage/dentist/edit_dentist.html', context)

@login_required
def delete_dentist(request, slug, dentist_id):
    clinic = get_object_or_404(Clinic, slug=slug, owner=request.user)
    dentist = get_object_or_404(Dentist, id=dentist_id, clinic=clinic)
    if request.method == 'POST':
        user = dentist.dentist
        dentist.delete()
        user.delete()
        messages.success(request, "Nha sĩ đã được xóa thành công!")
        return redirect('list_dentists', slug=slug)
    context = {
        'dentist': dentist,
        'clinic': clinic,
    }
    return render(request, 'app_manage/dentist/delete_dentist.html', context)


def clinic_schedule(request, slug):
    clinic = get_object_or_404(Clinic, slug=slug)
    schedules = Schedule.objects.filter(clinic=clinic)
    context = {
        'clinic': clinic,
        'schedules': schedules,
    }
    return render(request, 'app_manage/clinic/clinic_schedule.html', context)


@login_required
def cancel_schedule_clinic(request, slug, schedule_id):
    clinic = get_object_or_404(Clinic, slug=slug, owner=request.user)
    schedule = get_object_or_404(Schedule, id=schedule_id, clinic=clinic)
    if request.method == 'POST':
        schedule.delete()
        messages.success(request, "Lịch làm việc đã được xóa thành công!")
        return redirect('clinic_schedule', slug=slug)

    context = {
        'schedule': schedule,
        'clinic': clinic,
    }
    return render(request, 'app_manage/clinic/delete_schedule_clinic.html', context)

@login_required(login_url='login')  # Chỉ cho phép người dùng đã đăng nhập
def add_schedule_clinic(request, slug):
    clinic = get_object_or_404(Clinic, slug=slug, owner=request.user)
    if request.method == 'POST':
        form = ScheduleForm(request.POST, clinic=clinic)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.clinic = clinic
            schedule.save()
            messages.success(request, "Lịch làm việc đã được thêm thành công!")
            return redirect('clinic_schedule', slug=slug)
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin.")
    else:
        form = ScheduleForm(clinic=clinic)

    context = {
        'form': form,
        'clinic': clinic,
    }
    return render(request, 'app_manage/clinic/add_schedule_clinic.html', context)


@login_required(login_url='login')  # Chỉ cho phép người dùng đã đăng nhập
def dashboard(request):
    if request.user.role == 'ClinicOwner':
        total_clinics = Clinic.objects.filter(owner=request.user).count()
        total_dentists = Dentist.objects.filter(clinic__owner=request.user).count()
        clinics = Clinic.objects.filter(owner=request.user)
        dentists = Dentist.objects.filter(clinic__owner=request.user)

        context = {
            'total_clinics': total_clinics,
            'total_dentists': total_dentists,
            'clinics': clinics,
            'dentists': dentists,
        }
        return render(request, 'app_manage/dashboard.html', context)
    
    elif request.user.role == 'Dentist':
        try:
            dentist = Dentist.objects.get(dentist=request.user)
        except Dentist.DoesNotExist:
            messages.error(request, "Nha sĩ không tồn tại.")
            return redirect('home')  # Chuyển hướng đến trang chủ hoặc trang khác nếu cần

        total_schedule = Schedule.objects.filter(dentist=dentist).count()
        total_appointment = Appointment.objects.filter(dentist=dentist).count()
        
        schedules = Schedule.objects.filter(dentist=dentist)
        appointments = Appointment.objects.filter(dentist=dentist)

        context = {
            'dentist': dentist,
            'total_schedule': total_schedule,
            'total_appointment': total_appointment,
            'schedules': schedules,
            'appointments': appointments,
        }
        return render(request, 'app_manage/dashboard.html', context)

    else:
        messages.error(request, "Vai trò người dùng không hợp lệ.")
        return redirect('home')  # Chuyển hướng đến trang chủ hoặc trang khác nếu cần

def search_view(request):
    query = request.GET.get('q')
    if query:
        results = search_all(query)
    else:
        results = {
            'clinics': [],
            'dentists': [],
            'categories': []
        }
    return render(request, 'app_manage/search_results.html', {'results': results})




