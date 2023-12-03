from django.db import models

# # 위치 정보->차관, 인대 등
# class where(models.Model):
#     # 차관
#     where = models.CharField(max_length=10)
#
# 위치 정보-> 이걸... 카테고리로 나눌까? 긁적

# 강의실 정보
class Lectureroom(models.Model):
    #어디?(차관?, 인대? 등)
    where = models.CharField(max_length=10)

    #몇호?
    number = models.IntegerField()

    #수업 -> 여러개 추가할 수 있게 해야함
    lecture = models.DateTimeField()

    def __str__(self):
        return f'[{self.where}]{self.number}호'
