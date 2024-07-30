from django.db import models
from account.models import CustomUser
from gyms.models import PT

class Event(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    # schedule_calendar_id = models.CharField(max_length=200)
    pt = models.ForeignKey(PT, on_delete=models.CASCADE, null=True)
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True) # 사용자 구분
    title = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.CharField(max_length=1000, null=True)
    background_color = models.CharField(max_length=20, default='blue')
    # 7/23 추가
    pt = models.ForeignKey(PT, on_delete=models.CASCADE, null=True)#cascade,null,blank=True 추가 필요?

    def __str__(self):
        return self.title
    


# 데이터 삭제 -> 모델 초기화 -> 마이그레이션 -> 캘린더 추가 -> 캘린더 삭제