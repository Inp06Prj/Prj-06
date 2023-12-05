from django.urls import path
# from .views import CollegeAndFloorView, RoomNumView, RoomReservationTableView
from . import views

urlpatterns = [
    # # path('collegeAndFloor/',views.collegeAndFloor, name='college_and_floor'),
    path('collegeAndFloor/', views.college_and_floor, name='choice college&floor'),
    # # path('',views.FloorList.as_view()),
    # path('roomNum/<str:college_name><int:floor>/',views.roomNum, name='choice classroom'),
    path('cha3/', views.cha3, name='차미리관 3층'),
    # # path('collegeAndFloor/<str:college_floor>/', RoomNumView.as_view(), name='room_num'),

    # path('collegeAndFloor/<str:college_floor>/<int:room_num>/', RoomReservationTableView.as_view(), name='room_reservation_table'),
    path('roomReservationTable/', views.room_reservation, name='reservation table'),
    path('get_events/', views.get_events, name='get_events'),
    path('set_all_day_event/', views.set_all_day_event, name='set_all_day_event'),
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete_event/<int:event_id>/', views.delete_schedule, name='delete_schedule'),




    path('get_current_user/', views.get_current_user, name='get_current_user'),
]