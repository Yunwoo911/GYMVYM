from django.db import models
from account import CustomUser

# Create your models here.
class Equipment(models.Model): # 헬스장 기구
    equipment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True) #사용자
    equipment_name = models.CharField(max_length=100) #이름

class EquipmentReservation(models.Model): # 기구 예약
    res_id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE) # 기구
    start_time = models.DateTimeField(null=True) # 시작 시간
    end_time = models.DateTimeField(null=True) # 종료 시간

class EquipmentInUse(models.Model): # 사용중인 기구
    use_equip_id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)