from django.db import models
from django.contrib.auth.models import User, Group


class Pro_User(models.Model):
    UNIV_OFFICE_CHOICES = [
        ('약학대학', '약학대학'),
        ('차미리사관', '차미리사관'),
        ('인문대학', '인문대학'),
        ('예술대학', '예술대학'),
        # 나중에 더 추가할 예정 (이 기능이 실제로 구현된다고 하면)
    ]

    MAJOR_CHOICES = [
        ('컴퓨터공학전공', '컴퓨터공학전공'),
        ('사이버보안전공', '사이버보안전공'),
        ('IT 미디어 공학전공', 'IT 미디어 공학전공'),
        # 나중에 더 추가할 예정 (이 기능이 실제로 구현된다고 하면)
    ]
    UNIV_CHOICES = [
        ('약학대학', '약학대학'),
        ('글로벌융합대학', '글로벌융합대학'),
        ('과학기술대학', '과학기술대학'),
        ('미술대학', '미술대학'),
        # 나중에 더 추가할 예정 (이 기능이 실제로 구현된다고 하면)
    ]

    # id_number = models.CharField(max_length=10, unique=True)
    # password = models.CharField(max_length=128)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    user_name = models.CharField(max_length=8, verbose_name="교수님 이름", null=True)

    is_student = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=True)

    univ = models.CharField(choices=UNIV_CHOICES, max_length=100, null=True)
    major = models.CharField(choices=MAJOR_CHOICES, max_length=100, null=True)

    phone_number = models.CharField(max_length=15, verbose_name="전화번호", null=True)

    office_building = models.CharField(choices=UNIV_OFFICE_CHOICES, max_length=100, verbose_name="단과대 건물", null=True)
    office_floor = models.CharField(max_length=50, verbose_name="건물 층", null=True)
    office_room_number = models.CharField(max_length=500, verbose_name="호", null=True)


    def __str__(self):
         return f'[{self.major}] {self.user_name}(교수) {self.office_building} - {self.office_room_number}'


class Calendar(models.Model):
    user = models.ForeignKey(Pro_User, on_delete=models.CASCADE) # 사용자 (Pro_User 테이블의 PK)
    title = models.CharField(max_length=100) # 이벤트 제목
    start = models.DateTimeField('Start Date') # 이벤트 시작일시
    end = models.DateTimeField('End Date  ') # 이벤트 종료일시
    allDay = models.BooleanField(default=False) # 이벤트가 종일 지속되는지 여부

    def __str__(self):
        start_str = self.start.strftime('%Y-%m-%d %H:%M')  # Format as 'YYYY-MM-DD HH:MM'
        end_str = self.end.strftime('%Y-%m-%d %H:%M')  # Format as 'YYYY-MM-DD HH:MM'

        return f'{self.user.user_name} 교수 - {self.title} => {start_str} ~ {end_str}'
