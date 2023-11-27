from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


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
    create_date = models.DateTimeField()

    def __str__(self):
        return self.title


class Reply(models.Model):
    """
        reply: Reply -> Board 연결관계
        comment: 댓글내용
        rep_date: 작성일
    """
    reply = models.ForeignKey(Board, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, null=False)
    rep_date = models.DateTimeField()

    def __str__(self):
        return self.comment