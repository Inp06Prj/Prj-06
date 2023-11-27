from django.urls import path
from .views import custom_login, custom_logout, main_view
from . import views

urlpatterns = [
    # 학생들한테 보여지는 페이지들
    
    path('login/', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('main/', views.main_view, name='main'),
    path('my_page/', views.mypage, name='my_page'),

]

