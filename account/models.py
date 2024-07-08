from django.db import models
from django.contrib.auth.models import User

# 상속?
class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)     # 1대1 관계
    # user_id = models.AutoField(primary_key=True)
    nfc_uid = models.CharField(max_length=100, unique=True, null=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    detail_address = models.CharField(max_length=255, null=True)
    usertype = models.IntegerField()
    nickname = models.CharField(max_length=100, null=True)
    user_image = models.ImageField(upload_to='profile_images', null=True)
    birth = models.DateField()
    gender = models.CharField(max_length=10)
    # is_superuser = models.BooleanField(default=False)

class Owner(models.Model):
    owner_id = models.AutoField(primary_key=True)
    owner_name = models.CharField(max_length=100)

class Gym(models.Model):
    gym_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    gym_name = models.CharField(max_length=100)
    gym_address = models.CharField(max_length=255)

class Trainer(models.Model):
    trainer_id = models.AutoField(primary_key=True)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    trainer_name = models.CharField(max_length=100)
    certificate = models.CharField(max_length=100, null=True)
    trainer_image = models.ImageField(upload_to='trainer_images', null=True)

class GymMember(models.Model):
    member_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    join_date = models.DateField()
    membership_type = models.CharField(max_length=100)
    expiry_date = models.DateField()
    recent_joined_date = models.DateField()
    recent_membership = models.CharField(max_length=100)
    recent_expiry = models.DateField()
    renewal_status = models.BooleanField(default=False)
    renewal_count = models.IntegerField(default=0)

class PT(models.Model):
    pt_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(GymMember, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    member_name = models.CharField(max_length=100)
    registration_date = models.DateField()
    pt_end_date = models.DateField()
    duration = models.IntegerField()

class Equipment(models.Model): # 헬스장 기구
#    member = models.ForeignKey(GymMember, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) #사용자
    equipment_id = models.AutoField(primary_key=True)
    equipment_name = models.CharField(max_length=100) #이름

class EquipmentReservation(models.Model): # 기구 예약
    res_id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE) # 기구
    start_time = models.DateTimeField(null=True) # 시작 시간
    end_time = models.DateTimeField(null=True) # 종료 시간

class EquipmentInUse(models.Model): # 사용중인 기구
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

class VisitLog(models.Model): # 출입관리
    visitlog_id = models.AutoField(primary_key=True)
    nfc_uid = models.CharField(max_length=30, null=True)
    enter_time = models.DateTimeField()
    exit_time = models.DateTimeField(null=True)
    fields = models.CharField(max_length=100, null=True)

class DataAnalysis(models.Model):
    analysis_id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    equipment_use_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    member = models.ForeignKey(GymMember, on_delete=models.CASCADE)
    fields = models.CharField(max_length=100, null=True)

class ChatRoom(models.Model):
    chatroom_id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(User, related_name='chatrooms_as_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='chatrooms_as_user2', on_delete=models.CASCADE)
    chatroom_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_name_add=True)

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    send_id = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receive_id = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)    
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)