from django.urls import path
from .views import custom_login, custom_logout, main_view, professor_list, professor_schedule
from . import views

# 황민지&김여름

urlpatterns = [
    # 학생들한테 보여지는 페이지들
    
    path('login/', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('main/', views.main_view, name='main'),
    path('my_page/', views.my_page, name='my_page'),

    path('professors/', professor_list, name='professor_list'),
    path('professors/<int:professor_id>/', professor_schedule, name='professor_schedule'),

    path('univ_and_major_list/', views.univ_and_major, name='univ_and_major_list'),

    # 여름님 코드
    path('create_reservation/<int:professor_id>/', views.create_reservation, name='create_reservation'),
]

