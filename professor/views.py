from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseNotAllowed
from .models import Calendar
import json
from .forms import CalendarEditForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .models import Pro_User

from login.models import UserProfile, Reserve

def pro_login(request):
    if request.user.is_authenticated:
        return redirect(reverse(pro_main_view))

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = form.get_user()

            if user is not None:
                # Check group membership
                professor_group = Group.objects.get(name='Professor')
                if user.groups.filter(name='Professor').exists():
                    login(request, user)
                    return redirect(reverse(pro_main_view))
                else:
                    messages.error(request, '로그인 실패: 폼이 유효하지 않음')
            # else:
            #     messages.error(request, '로그인 실패: 사용자 인증 실패')
        else:
            messages.error(request, '로그인 실패: 폼이 유효하지 않음')
    else:
        form = AuthenticationForm()

    return render(request, 'professor/login.html', {'form': form})


def pro_logout(request):
    logout(request)
    messages.success(request, '(교수) 로그아웃 되었습니다.')
    return redirect(reverse('pro_login'))


def pro_main_view(request):
    pro_users = Pro_User.objects.order_by('-pk')

    context = {'pro_users': pro_users}

    if request.user.is_authenticated:
        # 인증된 사용자에게 메인 페이지를 렌더링합니다.
        context['user'] = request.user  # 사용자 정보를 context에 추가

        return render(request, 'professor/main.html', context)
    else:
        # 미인증 사용자에게 로그인 페이지로 리디렉션합니다.
        return redirect(reverse('pro_login'))


def my_page(request):
    if request.user.is_authenticated:
        # 교수 정보 가져오기
        pro_user = Pro_User.objects.get(user=request.user)

        reservations = Reserve.objects.filter(professor=pro_user)
        context = {'user': request.user, 'pro_user': pro_user, 'reservations': reservations}

        # context = {'user': request.user, 'pro_user': pro_user}
        return render(request, 'professor/my_page.html', context)
    else:
        return redirect(reverse('pro_login'))


# 교수님이 따로 자신의 스케줄을 등록
def schedule_index(request):
    # 오늘날짜구함
    today = date.today()

    context = {'today_ymd' : today.strftime('%Y-%m-%d')}
    if request.user.is_authenticated:
        # 인증된 사용자에게 메인 페이지를 렌더링합니다.
        # context['user'] = request.user  # 사용자 정보를 context에 추가

        return render(request, 'professor/index.html', context)
    else:
        # 미인증 사용자에게 로그인 페이지로 리디렉션합니다.
        return redirect(reverse('pro_login'))


def get_events(request):
    if request.user.is_authenticated:
        start_date = request.GET.get('start')
        end_date = request.GET.get('end')

        if not start_date or not end_date:
            return HttpResponseBadRequest("Invalid start or end date")

        pro_user = Pro_User.objects.get(user=request.user)
        data = list(Calendar.objects.filter(user=pro_user, start__gte=start_date[0:10], end__lte=end_date[0:10]).values())

        return JsonResponse(data, safe=False)
    else:
        return redirect(reverse('pro_login'))


# 학생들한테 교수님의 스케줄 보내주려고 만들었음...
def get_professor_events(request, professor_id):
    try:
        pro_user = Pro_User.objects.get(pk=professor_id)
        data = list(Calendar.objects.filter(user=pro_user).values())
        return JsonResponse(data, safe=False)
    except Pro_User.DoesNotExist:
        return HttpResponseBadRequest("Invalid professor ID")


def set_all_day_event(request):
    if request.user.is_authenticated:
        pro_user = Pro_User.objects.get(user=request.user)
        data = json.loads(request.body.decode('utf-8'))
        calendar = Calendar(user=pro_user, title=data['title'], start=data['start'], end=data['end'], allDay=data['allDay'])
        calendar.save()
        return JsonResponse({"result": "success", "eventId": calendar.id}, safe=False)
    else:
        return redirect(reverse('pro_login'))


def edit_event(request, event_id):
    calendar_event = get_object_or_404(Calendar, id=event_id)
    if request.method == 'POST':
        form = CalendarEditForm(request.POST, instance=calendar_event)
        if form.is_valid():
            form.save()

            # Redirect to the schedule_index page
            return redirect(reverse('schedule_index'))
    else:
        form = CalendarEditForm(instance=calendar_event)

    return render(request, 'professor/edit_event.html', {'form': form, 'event': calendar_event})


def delete_schedule(request, event_id):
    if request.user.is_authenticated:
        calendar_event = get_object_or_404(Calendar, id=event_id)
        if request.method == 'POST':
            print('Deleting event:', calendar_event)
            calendar_event.delete()
            print('Event deleted successfully!')
            return redirect(reverse('schedule_index'))
        # Handle other HTTP methods if necessary
        return HttpResponseNotAllowed(['POST'])
    else:
        return redirect(reverse('pro_login'))


def update_reservation_status(request, reservation_id, new_status): #수락/거절
    if request.method == 'POST':
        reservation = get_object_or_404(Reserve, pk=reservation_id)

        # 새로운 상태(new_status)가 유효한지 확인
        if new_status in ['accepted', 'rejected']:
            reservation.status = new_status
            reservation.save()

    # 마이페이지로 리디렉션
    return redirect('pro_my_page')