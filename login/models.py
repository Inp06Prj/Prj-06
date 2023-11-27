from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    UNIV_CHOICES = [
        ('약학대학', '약학대학'),
        ('글로벌융합대학', '글로벌융합대학'),
        ('과학기술대학', '과학기술대학'),
        ('미술대학', '미술대학'),
        # 나중에 더 추가할 예정 (이 기능이 실제로 구현된다고 하면)
    ]

    MAJOR_CHOICES = [
        ('컴퓨터공학전공', '컴퓨터공학전공'),
        ('사이버보안전공', '사이버보안전공'),
        ('IT 미디어 공학전공', 'IT 미디어 공학전공'),
        # 나중에 더 추가할 예정 (이 기능이 실제로 구현된다고 하면)
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    is_student = models.BooleanField(default=True)
    is_professor = models.BooleanField(default=False)


    # 특정 유저 생성
    # user = User.objects.create_user(username='학번이름', password='비밀번호')
    # user.username -> 학번으로 생각할 예정
    # user.password -> 비밀번호로 생각할 예정

    phone_number = models.CharField(max_length=15, verbose_name="전화번호", null=True)
    user_name = models.CharField(max_length=8, verbose_name="학생 이름", null=True)
    univ = models.CharField(choices=UNIV_CHOICES, max_length=18, verbose_name="단과대학", null=True)
    major = models.CharField(choices=MAJOR_CHOICES, max_length=18, verbose_name="전공", null=True)


    def __str__(self):
        return f'[{self.major}] {self.user.username} - {self.user_name}(학생)'
