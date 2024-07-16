import uuid
from django.utils import timezone
from django.utils.text import slugify
from faker import Faker
from account.models import CustomUser 
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
import random
from gyms.models import GymMember, Gym, Owner

# 더미 데이터 생성
fake = Faker()

# 사용자 데이터 생성 함수
def create_custom_user(i):
    username = f'user_{i}'
    email = f'user_{i}@example.com'
    phone_number = fake.port_number()
    address = fake.address()
    detail_address = fake.secondary_address()
    nickname = f'nickname_{i}'
    # user_image = 'static/default.png'
    birth = fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=90)
    usertype = fake.random_element(elements=(0, 1, 2))
    gender = fake.random_element(elements=('0', '1'))
    date_joined = timezone.now()
    last_login = timezone.now()

    user = CustomUser(
        user=uuid.uuid4(),
        nfc_uid=uuid.uuid4(),
        username=username,
        password=make_password('password'),  # 여기에서 비밀번호를 해시하여 저장합니다.
        phone_number=phone_number,
        email=email,
        address=address,
        detail_address=detail_address,
        nickname=nickname,
        user_image=False,
        birth=birth,
        usertype=usertype,
        gender=gender,
        date_joined=date_joined,
        last_login=last_login
    )
    user.save()


def create_dummy_owners(num_records):
    for _ in range(num_records):
        owner_name = fake.name()
        
        Owner.objects.create(
            owner_name=owner_name
        )


def create_dummy_gyms(num_records):
    owners = Owner.objects.all()

    if not owners:
        print("No owners found in the database. Please add some owners first.")
        return

    for _ in range(num_records):
        owner = random.choice(owners)
        gym_name = fake.company()
        gym_address = fake.address()

        Gym.objects.create(
            owner=owner,
            gym_name=gym_name,
            gym_address=gym_address
        )


def create_gym_member(num_records):
    users = CustomUser.objects.all()
    gyms = Gym.objects.all()
    
    for _ in range(num_records):
        user = random.choice(users)
        gym = random.choice(gyms)
        join_date = fake.date_this_decade()
        membership_type = fake.random_element(elements=("Basic", "Premium", "VIP"))
        expiry_date = join_date + timedelta(days=365)  # assuming 1 year membership
        recent_joined_date = fake.date_between_dates(date_start=join_date, date_end=expiry_date)
        recent_membership = fake.random_element(elements=("Basic", "Premium", "VIP"))
        recent_expiry = recent_joined_date + timedelta(days=365)
        renewal_status = fake.boolean()
        renewal_count = fake.random_int(min=0, max=5)

        GymMember.objects.create(
            user=user,
            gym=gym,
            join_date=join_date,
            membership_type=membership_type,
            expiry_date=expiry_date,
            recent_joined_date=recent_joined_date,
            recent_membership=recent_membership,
            recent_expiry=recent_expiry,
            renewal_status=renewal_status,
            renewal_count=renewal_count
        )


# 30개의 사용자 데이터 생성
# for i in range(100, 140):
#     create_custom_user(i)

# create_gym_member(100)  # 원하는 더미 데이터 수

# create_dummy_owners(50) # 원하는 더미 데이터 수

# create_dummy_gyms(50)