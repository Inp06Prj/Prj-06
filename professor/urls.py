from django.urls import path
from .views import pro_login, pro_logout, pro_main_view
from . import views

urlpatterns = [
    path('pro_login/', pro_login, name='pro_login'),
    path('pro_logout/', pro_logout, name='pro_logout'),
    path('pro_main/', views.pro_main_view, name='pro_main'),

    path('pro_schedule/', views.schedule_index, name='schedule_index'),
    path('get_events/', views.get_events, name='get_events'),
    path('set_all_day_event/', views.set_all_day_event, name='set_all_day_event'),
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
]