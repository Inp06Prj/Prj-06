from django.urls import path



# from login.views import custom_login, custom_logout, main_view



from . import views

urlpatterns = [
    path('', views.landing),


    # path('login/', views.custom_login, name='custom_login'),
    # path('logout/', views.custom_logout, name='custom_logout'),
    # path('main/', views.main_view, name='main'),
    # Add other URLs as needed
]