from datetime import date
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
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

    # title_options = ['수업', '점심', '출장', '회의', '귀가']

    if request.method == 'POST':
        form = CalendarEditForm(request.POST, instance=calendar_event)
        if form.is_valid():
            form.save()

            # Redirect to the schedule_index page
            return redirect(reverse('schedule_index'))
    else:
        form = CalendarEditForm(instance=calendar_event)

    return render(request, 'professor/edit_event.html', {'form': form, 'event_id': event_id})