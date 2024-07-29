from django.db import models
from django.core.validators import RegexValidator
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

phone_regex = RegexValidator(
    regex=r'^\d{3}-\d{4}-\d{4}$',
    message="Phone number must be entered in the format: 'OOO-OOOO-OOOO'."
)

class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('usertype', 2) # 일반유저 usertype : member로 기본설정
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('usertype', 0) # 관리자 usertype : owner로 기본설정
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
    ('0', 'Man'),
    ('1', 'Woman'),
    ]

    USERTYPE_CHOICES = [
    (0, 'Owner'),
    (1, 'Trainer'),
    (2, 'Member'),
    ]

    user = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # UUID 사용 : 중복 방지, 난수 기반으로 보안 상승, 식별자 생성시 충돌방지
    nfc_uid = models.CharField(unique=True, null=True, blank=True, editable=True)
    username = models.CharField(max_length=100,blank=False)
    phone1 = models.CharField(max_length=3, validators=[phone_regex])
    phone2 = models.CharField(max_length=4, validators=[phone_regex])
    phone3 = models.CharField(max_length=4, validators=[phone_regex])
    email = models.EmailField(unique=True, blank=False, null=False)
    address = models.CharField(max_length=255)
    detail_address = models.CharField(max_length=255, null=False)
    nickname = models.CharField(max_length=100, null=False, default='', unique=True)
    user_image = models.ImageField(upload_to='user_image', null=True, default='default.png')
    birth = models.DateField(null=False)
    usertype = models.IntegerField(choices=USERTYPE_CHOICES,default=2)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    is_staff = models.BooleanField(null=True, blank=True)
    description = models.CharField(null=True, blank=True, max_length=255)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    gym_entry_count = models.PositiveIntegerField(default=0, blank=True, null=True) # 7/16 헬스장 입장 횟수 추가
    gym_manual_exit_count = models.PositiveIntegerField(default=0, blank=True, null=True) # 7/16 헬스장 수동 퇴실 횟수 추가
    manual_exit_rate = models.DecimalField(
        default=100.0,
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        blank=True, null=True
    ) # 7/16 수동 퇴실율 추가

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_userimage(self):
        return settings.WEBSITE_URL + self.user_image.url

def calculate_manual_exit_rate(self):  # 7/16 수동 퇴실율 계산 함수 추가
        if self.gym_entry_count > 0:
            self.manual_exit_rate = float(self.gym_manual_exit_count) / self.gym_entry_count * 100
        else:
            self.manual_exit_rate = 100.0
        self.save()

class Meta:
        constraints = [
            models.UniqueConstraint(fields=['phone1', 'phone2', 'phone3'], name='unique_phone_number')
        ]

class EmailVerification(models.Model) :
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    verification_code = models.UUIDField(default=uuid.uuid4)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    expires_at = models.DateField()

    def save(self, *args, **kwargs) :
        if not self.expires_at :
            self.expires_at = self.created_at + timedelta(minutes=5)
            super().save(*args, **kwargs)