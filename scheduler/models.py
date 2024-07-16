from django.db import models
from account.models import CustomUser

class Event(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True) # 사용자 구분
    title = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField()
    background_color = models.CharField(max_length=20, default='blue')

    def __str__(self):
        return self.title