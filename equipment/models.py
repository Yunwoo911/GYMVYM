from django.db import models
from account.models import CustomUser
from django.utils import timezone
from gyms.models import Gym

# Create your models here.
class Equipment(models.Model): # 헬스장 기구
    equipment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True) # 사용자 구분
    equipment_name = models.CharField(max_length=50) #이름
    # 추가 필드
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE) # 헬스장 아이디
    equipment_type = models.CharField(max_length=50) # 기구 종목 (유산소, 웨이트_상체, 웨이트_하체)
    equipment_description = models.TextField(null=True, blank=True) # 기구 설명
    equipment_image = models.ImageField(upload_to='equipment_images/', null=True, blank=True) # 기구 이미지

class TimeSlot(models.Model):
    TIMESLOT_CHOICES = [
        ('18:00 - 18:30', '18:00 - 18:30'),
        ('18:30 - 19:00', '18:30 - 19:00'),
        ('19:00 - 19:30', '19:00 - 19:30'),
        ('19:30 - 20:00', '19:30 - 20:00'),
        ('20:00 - 20:30', '20:00 - 20:30'),
        ('20:30 - 21:00', '20:30 - 21:00'),
    ]
    timeslot_id = models.AutoField(primary_key=True)
    slot = models.CharField(max_length=20, choices=TIMESLOT_CHOICES, unique=True)

class EquipmentReservation(models.Model): # 기구 예약
    res_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True) # 사용자 구분
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE) # 기구
    res_start_time = models.DateTimeField(null=True) # 시작 시간
    res_end_time = models.DateTimeField(null=True) # 종료 시간
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE) # 예약 시간 슬롯
    # status = models.CharField(max_length=20, default='confirmed') # 예약 상태 (예: pending, confirmed, cancelled)

class EquipmentInUse(models.Model): # 사용중인 기구
    use_equip_id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) # 사용자 구분
    res = models.ForeignKey(EquipmentReservation, on_delete=models.SET_NULL, null=True, blank=True) # 예약이 없는 경우를 고려하여 비식별 관계로 설정
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    #  현재 사용 중인지 여부 확인
    def is_currently_in_use(self):
        now = timezone.now()
        # 기구 사용이 이미 시작되었는지 여부를 확인
        # 기구 사용이 아직 끝나지 않았는지 여부를 확인
        return self.start_time <= now and (self.end_time is None or self.end_time >= now)