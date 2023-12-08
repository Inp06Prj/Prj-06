from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


# 황민지
class Board(models.Model):
    """
    title: 제목
    content: 내용
    author: 작성자 (User 모델과의 연결)
    create_date: 작성일
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False)
    content = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # create_date = models.DateTimeField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# 황민지
class Reply(models.Model):
    """
        reply: Reply -> Board 연결관계
        comment: 댓글내용
        rep_date: 작성일
    """
    id = models.AutoField(primary_key=True)
    reply = models.ForeignKey(Board, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, null=False)
    rep_date = models.DateTimeField('Reply Date', default=timezone.now)

    anonymous_id = models.IntegerField(null=True, blank=True)  # 추가: 익명 번호

    def save(self, *args, **kwargs):
        # 댓글 작성 시 익명 번호 부여
        if not self.anonymous_id:
            # 해당 게시글에 작성된 댓글 중 가장 큰 익명 번호 가져오기
            last_anonymous_id = Reply.objects.filter(reply=self.reply).aggregate(models.Max('anonymous_id'))[
                'anonymous_id__max']
            # 가져온 익명 번호가 존재하면 +1, 없으면 1로 설정
            self.anonymous_id = last_anonymous_id + 1 if last_anonymous_id else 1
        super().save(*args, **kwargs)


    def __str__(self):
        return self.comment