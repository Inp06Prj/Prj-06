from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
#from professor.models import Pro_User


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

    # username = models.CharField(max_length=8, verbose_name="학생이름", null=True)

    def __str__(self):
        return f'[{self.major}] {self.user.username} - {self.user_name}(학생)'


class Reserve(models.Model):
    student = models.ForeignKey('login.UserProfile', related_name='login_reserve_requested', on_delete=models.CASCADE)
    professor = models.ForeignKey('professor.Pro_User', related_name='professor_reserve_received', on_delete=models.CASCADE)
    status_choices = [('pending', _('대기')), ('accepted', _('수락')), ('rejected', _('거절'))]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    reason = models.TextField(default='')

    def get_status_display_korean(self):
        return dict(self.status_choices)[self.status]

    def __str__(self):
        return f"{self.student.major} {self.student.user_name} {self.time} {self.reason} -> {self.professor.user_name}: {self.status}"


from professor.models import Calendar


@receiver(pre_save, sender=Reserve)
def update_calendar_on_accepted(sender, instance, **kwargs):

    if instance.status == 'accepted' and instance.pk is not None:
        try:
            start_datetime = timezone.datetime.combine(instance.date, instance.time)
            end_datetime = timezone.datetime.combine(instance.date, instance.time)

            # 수정된 부분: professor 필드에 대한 Pro_User 객체 얻기
            professor_user = instance.professor

            Calendar.objects.create(
                user=professor_user,
                title='상담',
                start=start_datetime,
                end=end_datetime,
                allDay=False
            )
            print("Calendar event created successfully.")
        except Exception as e:
            print(f"Error creating calendar event: {e}")

