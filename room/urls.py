from django.urls import path
# from .views import CollegeAndFloorView, RoomNumView, RoomReservationTableView
from . import views

# 오수연
urlpatterns = [
    path('collegeAndFloor/', views.college_and_floor, name='choice college&floor'),
    path('cha3/', views.cha3, name='차미리관 3층'),

    path('roomReservationTable/', views.room_reservation, name='reservation table'),
    path('get_events/', views.get_events, name='get_events'),
    path('set_all_day_event/', views.set_all_day_event, name='set_all_day_event'),

    path('get_current_user/', views.get_current_user, name='get_current_user'),
]