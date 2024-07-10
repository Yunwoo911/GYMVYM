from django.db import models
from account.models import CustomUser
from django.utils import timezone

# Create your models here.
class Equipment(models.Model): # 헬스장 기구
    equipment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True) #사용자
    equipment_name = models.CharField(max_length=50) #이름

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

    
    #  현재 사용 중인지 여부 확인
    def is_currently_in_use(self):
        now = timezone.now()
        # 기구 사용이 이미 시작되었는지 여부를 확인
        # 기구 사용이 아직 끝나지 않았는지 여부를 확인
        return self.start_time <= now and (self.end_time is None or self.end_time >= now)
