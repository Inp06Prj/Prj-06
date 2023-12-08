from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse

from django.contrib.auth.models import Group
from room.models import RoomReservation, Calendar
from .models import UserProfile, Reserve
from room.models import Calendar as RoomCalendar
from room.models import Room


# 황민지
def custom_login(request):
    if request.user.is_authenticated:
        return redirect(reverse('main'))

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = form.get_user()

            if user is not None:
                # Check group membership
                student_group = Group.objects.get(name='Student')
                if user.groups.filter(name='Student').exists():
                    login(request, user)
                    return redirect(reverse(main_view))
                else:
                    messages.error(request, '로그인 실패: 폼이 유효하지 않음')
        else:
            messages.error(request, '로그인 실패: 폼이 유효하지 않음')
    else:
        form = AuthenticationForm()

    return render(request, 'login/login.html', {'form': form})


# 황민지
def custom_logout(request):
    logout(request)
    messages.success(request, '(학생) 로그아웃 되었습니다.')
    return redirect(reverse('custom_login'))  # 여기서 'main'은 당신이 메인 페이지 URL 패턴에 지정한 이름입니다.


# 황민지
def main_view(request):
    stu_users = UserProfile.objects.order_by('-pk')
    context = {'stu_users': stu_users}

    if request.user.is_authenticated:
        # 인증된 사용자에게 메인 페이지를 렌더링합니다.
        context['user'] = request.user  # 사용자 정보를 context에 추가
        return render(request, 'login/main.html', context)
    else:
        # 미인증 사용자에게 로그인 페이지로 리디렉션합니다.
        return redirect(reverse('custom_login'))


# 황민지&김여름
@login_required(login_url='custom_login')
def my_page(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    # Existing code for reservations
    reservations = Reserve.objects.filter(student=user_profile).order_by('date')
    page_number = request.GET.get('page', 1)
    paginator = Paginator(reservations, 4)
    page_obj = paginator.get_page(page_number)

    # Fetch Calendar events from the room app
    room_calendar_events = RoomCalendar.objects.filter(student=user_profile).order_by('start')
    page_number_room = request.GET.get('page_room', 1)
    paginator_room = Paginator(room_calendar_events, 4)
    page_obj_room = paginator_room.get_page(page_number_room)

    professor = Pro_User.objects.all()

    context = {
        'user_profile': user_profile,
        'reservations': page_obj,
        'professor': professor,
        'room_calendar_events': page_obj_room,
        # 'room': room,
    }
    return render(request, 'login/mypage.html', context)



from professor.models import Pro_User, Calendar


# 황민지
def professor_schedule(request, professor_id):
    professor = get_object_or_404(Pro_User, pk=professor_id)
    schedule = Calendar.objects.filter(user=professor).values('id', 'title', 'start', 'end')
    schedule = Calendar.objects.filter(user=professor)
    return render(request, 'login/professor_schedule.html', {'professor': professor, 'schedule': schedule})


# 김여름
def professor_list(request):
    professors = Pro_User.objects.filter(is_professor=True)
    return render(request, 'login/professor_list.html', {'professors': professors})


# 김여름
def univ_and_major(request):
    user_profile = UserProfile.objects.get(user=request.user)
    major = user_profile.major
    univ = user_profile.univ

    return render(
        request,
        'login/univ&major.html',
        {
            'univ': univ,
            'major': major,
        }
    )


# 김여름
def create_reservation(request, professor_id):
    if request.method == 'POST':
        student = request.user.userprofile
        # professor = get_object_or_404(Pro_User, pk=professor_id)
        professor = get_object_or_404(Pro_User, id=professor_id)
        reservation_date = request.POST['reservation_date']
        reservation_time = request.POST['reservation_time']
        reservation_reason = request.POST['reservation_reason']
        reservation = Reserve.objects.create(
            student=student,
            professor=professor,
            date=reservation_date,
            time=reservation_time,
            reason=reservation_reason
        )
        reservation.save()

        # 디버깅을 위해 예약 정보를 콘솔에 출력
        print(f"Reservation created: {reservation}")

        # POST 요청 이후에 마이페이지로 리다이렉트
        return redirect(reverse('professor_schedule', kwargs={'professor_id': professor_id}))


    return render(request, 'login/professor_schedule.html')
