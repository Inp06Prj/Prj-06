from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),


    path('', include('single_pages.urls')),
    # 대문 페이지 -> 학생 로그인 페이지으로 갈건지, 교수자 로그인 페이지로 갈건지 물어봄

    path('stu/', include('login.urls')), # 학생자 로그인 기능 + 마이페이지 등 학생들의 정보
    path('board/', include('board.urls')), # 게시판 기능 <- 학생만 접근 가능

    path('pro/', include('professor.urls')), # 교수님 로그인 기능 + 교수님 시간 예약 등 교수님의 정보

    
]
