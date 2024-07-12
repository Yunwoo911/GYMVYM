import uuid
from django.utils import timezone
from django.utils.text import slugify
from faker import Faker
from account.models import CustomUser 
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
import random
from gyms.models import GymMember, Gym, Owner, PersonalInfo

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


def create_dummy_personal_info():
    # GymMember 객체들을 가져옵니다.
    gym_members = GymMember.objects.all()

    for gym_member in gym_members:
        personal_info = PersonalInfo(
            gym_member_id=gym_member,
            height=random.uniform(150.0, 200.0),
            weight=random.uniform(50.0, 100.0),
            medical_conditions="None",
            medications="None",
            frequency=random.randint(1, 7),
            types=random.choice(["Cardio", "Strength", "Flexibility"]),
            intensity=random.choice(["Low", "Moderate", "High"]),
            goals=random.choice(["Lose weight", "Gain muscle", "Improve endurance"]),
            diet_habits=random.choice(["Balanced diet", "High protein", "Low carb"]),
            sleep_pattern=random.choice(["5-6 hours", "7-8 hours", "9+ hours"]),
            stress_level=random.choice(["Low", "Medium", "High"]),
            smoking=random.choice([True, False]),
            smoking_amount=random.randint(0, 20) if random.choice([True, False]) else None,
            drinking=random.choice([True, False]),
            drinking_amount=random.randint(0, 10) if random.choice([True, False]) else None,
            body_fat_percentage=random.uniform(10.0, 25.0),
            muscle_mass=random.uniform(50.0, 80.0),
            basal_metabolic_rate=random.uniform(1200.0, 2000.0),
            bmi=random.uniform(18.5, 30.0),
            short_term_goals="Run 5km without stopping",
            long_term_goals="Complete a marathon",
            preferred_exercise_types=random.choice(["Running", "Weight lifting", "Yoga"]),
            available_times=random.choice(["Morning", "Afternoon", "Evening"])
        )

        personal_info.save()


def create_dummy_personal_info():
    # GymMember 객체들을 가져옵니다.
    gym_members = GymMember.objects.all()

    for gym_member in gym_members:
        personal_info = PersonalInfo(
            gym_member_if=gym_member,
            height=random.uniform(150.0, 200.0),
            weight=random.uniform(50.0, 100.0),
            medical_conditions="None",
            medications="None",
            frequency=random.randint(1, 7),
            types=random.choice(["Cardio", "Strength", "Flexibility"]),
            intensity=random.choice(["Low", "Moderate", "High"]),
            goals=random.choice(["Lose weight", "Gain muscle", "Improve endurance"]),
            diet_habits=random.choice(["Balanced diet", "High protein", "Low carb"]),
            sleep_pattern=random.choice(["5-6 hours", "7-8 hours", "9+ hours"]),
            stress_level=random.choice(["Low", "Medium", "High"]),
            smoking=random.choice([True, False]),
            smoking_amount=random.randint(0, 20) if random.choice([True, False]) else None,
            drinking=random.choice([True, False]),
            drinking_amount=random.randint(0, 10) if random.choice([True, False]) else None,
            body_fat_percentage=random.uniform(10.0, 25.0),
            muscle_mass=random.uniform(50.0, 80.0),
            basal_metabolic_rate=random.uniform(1200.0, 2000.0),
            bmi=random.uniform(18.5, 30.0),
            short_term_goals="Run 5km without stopping",
            long_term_goals="Complete a marathon",
            preferred_exercise_types=random.choice(["Running", "Weight lifting", "Yoga"]),
            available_times=random.choice(["Morning", "Afternoon", "Evening"])
        )

        personal_info.save()

# 30개의 사용자 데이터 생성
# for i in range(100, 140):
#     create_custom_user(i)

# create_gym_member(100)  # 원하는 더미 데이터 수

# create_dummy_owners(50) # 원하는 더미 데이터 수

# create_dummy_gyms(50)

create_dummy_personal_info()