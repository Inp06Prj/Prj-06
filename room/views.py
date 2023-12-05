from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.views.decorators.http import require_http_methods
from .models import *
from .forms import RoomReservationForm, CalendarEditForm
from django.urls import reverse
from login.models import UserProfile


def college_and_floor(request):
    rooms = Room.objects.all()
    building_floors = {}

    for room in rooms:
        building = room.building
        floor = room.floor

        if building not in building_floors:
            building_floors[building] = []

        if floor not in building_floors[building]:
            building_floors[building].append(floor)

    return render(
        request,
        'room/collegeAndFloor.html',
        {'building_floors': building_floors}
    )


def cha3(request):
    room_number = Room.objects.filter(building='차미리사관', floor=3)

    return render(
        request,
        'room/cha3.html',
        {'room_number': room_number}
    )



# @login_required
# def room_reservation(request):
#     if request.method == 'POST':
#         form = RoomReservationForm(request.POST)
#         if form.is_valid():
#             reservation = form.save(commit=False)
#             reservation.student = request.user
#             reservation.save()
#
#             # 이벤트를 캘린더에 추가
#             calendar_event = Calendar(
#                 title=f"{reservation.student.user_name} - {reservation.room} Reservation",
#                 start=reservation.start_time,
#                 end=reservation.end_time,
#                 allDay=False  # 예약은 하루 종일 이벤트가 아니므로 False
#             )
#             calendar_event.save()
#
#             print("Reservation and Calendar event saved successfully!")  # 디버깅을 위해 추가한 부분
#         else:
#             print("Form is not valid!")  # 디버깅을 위해 추가한 부분
#     else:
#         form = RoomReservationForm()
#
#     return render(request, 'room/roomReservationTable.html', {'form': form})


@login_required
def room_reservation(request):
    if request.method == 'POST':
        form = RoomReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.student = request.user
            reservation.save()

            # 이벤트를 캘린더에 추가
            calendar_event = Calendar(
                title=f"{reservation.student.user_name} - {reservation.room} Reservation",
                start=reservation.start_time,
                end=reservation.end_time,
                allDay=False  # 예약은 하루 종일 이벤트가 아니므로 False
            )
            calendar_event.save()

            print("Reservation and Calendar event saved successfully!")  # 디버깅을 위해 추가한 부분
        else:
            print("Form is not valid!")  # 디버깅을 위해 추가한 부분
    else:
        form = RoomReservationForm()

    return render(request, 'room/roomReservationTable.html', {'form': form})



def get_events(request):
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')

    if not start_date or not end_date:
        return HttpResponseBadRequest("Invalid start or end date")

    data = list(
        Calendar.objects.filter(start__gte=start_date[0:10], end__lte=end_date[0:10]).values()
    )

    return JsonResponse(data, safe=False)
# def get_events(request):
#     start_date_str = request.GET.get('start')
#     end_date_str = request.GET.get('end')
#
#     if not start_date_str or not end_date_str:
#         return HttpResponseBadRequest("Invalid start or end date")
#
#     try:
#         # 예상되는 날짜 형식으로 파싱
#         start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%S%z")
#         end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M:%S%z")
#
#         data = list(
#             Calendar.objects.filter(start__gte=start_date, end__lte=end_date).values()
#         )
#
#         return JsonResponse(data, safe=False)
#     except ValueError as e:
#         return HttpResponseBadRequest(f"Invalid date format: {e}")

def set_all_day_event(request):
    if request.user.is_authenticated:
        try:
            data = json.loads(request.body.decode('utf-8'))

            # 사용자 정보 가져오기
            stu_user = UserProfile.objects.get(user=request.user)

            # 캘린더 이벤트 추가
            calendar = Calendar(
                student=stu_user,
                title=data['title'],
                start=data['start'],
                end=data['end'],
                allDay=data['allDay']
            )
            calendar.save()

            return JsonResponse({"result": "success", "eventId": calendar.id}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "User not authenticated"}, status=403)


# def set_all_day_event(request):
#     if request.user.is_authenticated:
#         try:
#             data = json.loads(request.body.decode('utf-8'))
#
#             # 사용자 정보 가져오기
#             stu_user = UserProfile.objects.get(user=request.user)
#
#             # 캘린더 이벤트 추가
#             calendar = Calendar(
#                 student=stu_user,
#                 title=data['title'],
#                 start=data['start'],
#                 end=data['end'],
#                 allDay=data['allDay']
#             )
#             calendar.save()
#
#             return JsonResponse({"result": "success", "eventId": calendar.id}, safe=False)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
#     else:
#         return JsonResponse({"error": "User not authenticated"}, status=403)


def edit_event(request, event_id):
    calendar_event = get_object_or_404(Calendar, id=event_id)
    if request.method == 'POST':
        form = CalendarEditForm(request.POST, instance=calendar_event)
        if form.is_valid():
            form.save()
            return redirect(reverse('reservation table'))
    else:
        form = CalendarEditForm(instance=calendar_event)

    return render(request, 'room/edit_event.html', {'form': form, 'event': calendar_event})


def delete_schedule(request, event_id):
    if request.user.is_authenticated:
        calendar_event = get_object_or_404(Calendar, id=event_id)
        if request.method == 'POST':
            print('Deleting event:', calendar_event)
            calendar_event.delete()
            print('Event deleted successfully!')
            return redirect(reverse('reservation table'))
        return HttpResponseNotAllowed(['POST'])


def get_current_user(request):
    # 여기에서 사용자 정보를 가져오는 로직을 추가합니다.
    # 예시: 현재 로그인된 사용자의 정보를 JSON으로 반환
    if request.user.is_authenticated:
        user_data = {
            'id': request.user.id,
            'username': request.user.username,
            # 필요한 다른 사용자 정보들을 추가
        }
        return JsonResponse(user_data)
    else:
        return JsonResponse({'error': 'User not authenticated'})


