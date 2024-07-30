from django.db import models
from account.models import CustomUser


class Owner(models.Model):
    owner_id = models.AutoField(primary_key=True)
    owner_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.owner_name


class Gym(models.Model):
    gym_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    gym_name = models.CharField(max_length=100)
    gym_address = models.CharField(max_length=255)

# 7/23 수정
class Trainer(models.Model):
    trainer_id = models.AutoField(primary_key=True)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    # owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'usertype': 1}, null=True)
    trainer_name = models.CharField(max_length=100)
    certificate = models.CharField(max_length=500, null=True)
    trainer_image = models.ImageField(upload_to='trainer_images', null=True)
    

class GymMember(models.Model):
    member_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    join_date = models.DateField()
    membership_type = models.CharField(max_length=100)
    expiry_date = models.DateField()
    recent_joined_date = models.DateField()
    recent_membership = models.CharField(max_length=100)
    recent_expiry = models.DateField()
    renewal_status = models.BooleanField(default=False)
    renewal_count = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.user.username
    
    
# 2. 건강 상태
#    - 의료 상태(기존 질병, 부상 등):
#    - 복용 중인 약물:
#    - 의사의 소견서(필요한 경우):

# 3. 운동 경험 및 현재 상태
#    - 현재 운동 빈도(주당 몇 회):
#    - 현재 운동 종류:
#    - 운동 강도(낮음, 보통, 높음):
#    - 운동 목표(체중 감량, 근육 증가, 체력 향상 등):

# 4. 생활 습관
#    - 식습관(하루 식사 횟수, 주로 먹는 음식):
#    - 수면 패턴(하루 수면 시간):
#    - 스트레스 수준(낮음, 보통, 높음):
#    - 흡연 여부(예/아니오, 흡연량):
#    - 음주 여부(예/아니오, 음주량):

# 5. 신체 측정 정보
#    - 체지방률:
#    - 근육량:
#    - 기초대사량:

# 6. 운동 목표 및 선호도
#    - 단기 목표(3개월 이내):
#    - 장기 목표(1년 이내):
#    - 운동 선호도(개인 트레이닝, 그룹 운동, 특정 스포츠 등):
#    - 시간 가능 여부(하루 중 운동할 수 있는 시간대):
class PersonalInfo(models.Model):
    personal_if = models.AutoField(primary_key=True)
    gym_member_if = models.OneToOneField(GymMember, on_delete=models.CASCADE)
    height = models.FloatField()
    weight = models.FloatField()    

    medical_conditions = models.TextField()
    medications = models.TextField()

    frequency = models.IntegerField()  # per week
    types = models.CharField(max_length=255)
    intensity = models.CharField(max_length=50)
    goals = models.CharField(max_length=255)

    diet_habits = models.TextField()
    sleep_pattern = models.CharField(max_length=50)
    stress_level = models.CharField(max_length=50)
    smoking = models.BooleanField()
    smoking_amount = models.IntegerField(null=True, blank=True)
    drinking = models.BooleanField()
    drinking_amount = models.IntegerField(null=True, blank=True)

    body_fat_percentage = models.FloatField()
    muscle_mass = models.FloatField()
    basal_metabolic_rate = models.FloatField()
    bmi = models.FloatField()

    short_term_goals = models.TextField()
    long_term_goals = models.TextField()
    preferred_exercise_types = models.CharField(max_length=255)
    available_times = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.gym_member_if.user.username

class PT(models.Model):
    pt_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(GymMember, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    member_name = models.CharField(max_length=100)
    registration_date = models.DateField()
    pt_end_date = models.DateField()
    duration = models.IntegerField()

# 트레이너 권한 요청들을 관리하는 테이블
class TrainerRequest(models.Model):
    trainer_request_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT) # 유저
    requested_gym = models.ForeignKey(Gym, on_delete=models.PROTECT) # 트레이너 권한이 필요한 헬스장
    request_date = models.DateField(null=True, blank=True) # 요청 일자
    request_message = models.TextField(null=True, blank=True) # 요청 메세지
    approved = models.BooleanField(default=False) # 승인 여부
    approved_date = models.DateField(null=True, blank=True) # 승인 일자
<<<<<<< HEAD
    approved_by = models.ForeignKey(Owner, on_delete=models.PROTECT, null=True, blank=True,default=None) # 승인자
=======
    approved_by = models.ForeignKey(Owner, on_delete=models.PROTECT, null=True, blank=True,default=None) # 승인자

# 헬스장 소유 테이블
class Ownership(models.Model):
    ownership_id = models.AutoField(primary_key=True)
    gym = models.ForeignKey(Gym, on_delete=models.PROTECT)
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    note = models.TextField(null=True, blank=True) # 비고 필드

# 고용된 트레이너 테이블
class TrainerEmployment(models.Model):
    trainer_employment_id = models.AutoField(primary_key=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.PROTECT)
    gym = models.ForeignKey(Gym, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()

# 헬스장 회원권 테이블
class Membership(models.Model):
    membership_id = models.AutoField(primary_key=True)
    gym = models.ForeignKey(Gym, on_delete=models.PROTECT) # 헬스장
    membership_type = models.CharField(max_length=5,null=True, blank=True) # 회원권 종류
    membership_fee = models.FloatField(null=True, blank=True) # 회원권 지불 금액
    start_date = models.DateField(null=True, blank=True) # 회원권 시작일
    end_date = models.DateField(null=True, blank=True) # 회원권 종료일
    note = models.TextField(null=True, blank=True) # 비고 필드
>>>>>>> origin/visitlog
