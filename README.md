# GYM VYM
![멋사](likelion)
![멋사](grandprize)
헬스장 인원 파악 제휴 서비스

유저 dummy데이터 만드는 코드
```
import uuid
from django.utils import timezone
from account.models import CustomUser 
from django.utils.text import slugify
from faker import Faker

fake = Faker()

# 사용자 데이터 생성 함수
def create_custom_user(i):
    username = f'user_{i}'
    email = f'user_{i}@example.com'
    phone_number = fake.phone_number()
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
        password='password',  # 실제로는 해시된 비밀번호를 사용해야 합니다.
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

# 30개의 사용자 데이터 생성
for i in range(1, 31):
    create_custom_user(i)

```
