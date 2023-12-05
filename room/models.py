from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from login.models import UserProfile


class Room(models.Model):
    BUILDING_CHOICES = [
        ('약학대학', '약학대학'),
        ('차미리사관', '차미리사관'),
        ('인문사회관', '인문사회관'),
        ('미술대학', '미술대학'),
        # 추가 건물은 필요에 따라 확장
    ]

    floor = models.PositiveIntegerField(verbose_name="Floor")
    room_number = models.CharField(max_length=10, verbose_name="Room Number")
    building = models.CharField(choices=BUILDING_CHOICES, max_length=20, verbose_name="Building")

    def __str__(self):
        return f'{self.building} - Floor {self.floor}, Room {self.room_number}'


class Calendar(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)  # Add this line
    # student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)  # ForeignKey로 변경
    student = models.ForeignKey('login.UserProfile', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)  # 이벤트 제목
    start = models.DateTimeField('Start Date', default=timezone.now)  # 이벤트 시작일시
    end = models.DateTimeField('End Date  ', default=timezone.now)  # 이벤트 종료일시
    allDay = models.BooleanField(default=False)  # 이벤트가 종일 지속되는지 여부

    def __str__(self):
        if self.start: start_str = self.start.strftime('%Y-%m-%d %H:%M')
        else: start_str = "N/A" # Format as 'YYYY-MM-DD HH:MM'
        if self.end :end_str = self.end.strftime('%Y-%m-%d %H:%M')
        else : end_str = "N/A"# Format as 'YYYY-MM-DD HH:MM'
        return f'{self.student.user_name if self.student and self.student.user else "Unknown User"} - {self.title} - {start_str} to {end_str}'


class RoomReservation(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='room_reservations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.DateTimeField(verbose_name="Start Time")
    end_time = models.DateTimeField(verbose_name="End Time")

    def __str__(self):
        return f'{self.student.user_name} - {self.room} - {self.start_time} to {self.end_time}'


