from django.urls import path

from . import views

app_name = 'board'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:board_id>/', views.detail, name='detail'),
    path('write/', views.write, name='write'),
    path('write/write_board', views.write_board, name='write_board'),
    path('<int:board_id>/create_reply', views.create_reply, name='create_reply'),
    path('delete/<int:board_id>/', views.delete_board, name='delete_board'),
]