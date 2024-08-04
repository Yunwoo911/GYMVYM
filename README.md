![멋사](likelion.png)
![대상](grandprize.png)
![짐빔](gymvymlogo.png)

***

![Apache 2.0 License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![Python 3.10](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0.6-green?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.15.2-red)

***

NFC

![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-4B-red)
![RPi.GPIO](https://img.shields.io/badge/RPi.GPIO-0.7.0-yellow)
![MFRC522](https://img.shields.io/badge/mfrc522-1.6.0-blue)
![pillow](https://img.shields.io/badge/pillow-10.4.0-blue?logo=python&logoColor=white)

***

deployment

![gunicorn](https://img.shields.io/badge/gunicorn-22.0.0-green?logo=gunicorn&logoColor=white)
![PyYAML](https://img.shields.io/badge/PyYAML-6.0.1-blue)

***

![APScheduler](https://img.shields.io/badge/APScheduler-3.10.4-blue)
![asgiref](https://img.shields.io/badge/asgiref-3.8.1-lightgrey)
![certifi](https://img.shields.io/badge/certifi-2024.7.4-green)
![charset-normalizer](https://img.shields.io/badge/charset--normalizer-3.3.2-yellow)
![colorama](https://img.shields.io/badge/colorama-0.4.6-red)
![django-cors-headers](https://img.shields.io/badge/django--cors--headers-4.4.0-orange)
![django-widget-tweaks](https://img.shields.io/badge/django--widget--tweaks-1.5.0-blue)
![Faker](https://img.shields.io/badge/Faker-26.0.0-lightgreen)
![filelock](https://img.shields.io/badge/filelock-3.15.4-yellowgreen)
![fsspec](https://img.shields.io/badge/fsspec-2024.6.1-lightblue)
![idna](https://img.shields.io/badge/idna-3.7-purple)
![intel-openmp](https://img.shields.io/badge/intel--openmp-2021.4.0-blue)
![Jinja2](https://img.shields.io/badge/Jinja2-3.1.4-red)
![joblib](https://img.shields.io/badge/joblib-1.4.2-lightgrey)
![MarkupSafe](https://img.shields.io/badge/MarkupSafe-2.1.5-green)
![mkl](https://img.shields.io/badge/mkl-2021.4.0-blue)
![mpmath](https://img.shields.io/badge/mpmath-1.3.0-yellow)
![networkx](https://img.shields.io/badge/networkx-3.3-orange)
![packaging](https://img.shields.io/badge/packaging-24.1-lightblue)
![psycopg2-binary](https://img.shields.io/badge/psycopg2--binary-2.9.9-green)
![PyJWT](https://img.shields.io/badge/PyJWT-2.8.0-blue)
![python-dateutil](https://img.shields.io/badge/python--dateutil-2.9.0.post0-lightgrey)
![python-decouple](https://img.shields.io/badge/python--decouple-3.8-yellow)
![python-dotenv](https://img.shields.io/badge/python--dotenv-1.0.1-green)
![pytz](https://img.shields.io/badge/pytz-2024.1-red)
![regex](https://img.shields.io/badge/regex-2024.5.15-lightgreen)
![requests](https://img.shields.io/badge/requests-2.32.3-orange)
![safetensors](https://img.shields.io/badge/safetensors-0.4.3-yellow)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5.1-orange?logo=scikit-learn&logoColor=white)
![scipy](https://img.shields.io/badge/scipy-1.14.0-blue)
![six](https://img.shields.io/badge/six-1.16.0-lightgrey)
![sqlparse](https://img.shields.io/badge/sqlparse-0.5.0-green)
![sympy](https://img.shields.io/badge/sympy-1.13.0-red)
![tbb](https://img.shields.io/badge/tbb-2021.13.0-blue)
![threadpoolctl](https://img.shields.io/badge/threadpoolctl-3.5.0-lightblue)
![tokenizers](https://img.shields.io/badge/tokenizers-0.19.1-yellow)
![tqdm](https://img.shields.io/badge/tqdm-4.66.4-green)
![typing_extensions](https://img.shields.io/badge/typing__extensions-4.12.2-purple)
![tzdata](https://img.shields.io/badge/tzdata-2024.1-orange)
![tzlocal](https://img.shields.io/badge/tzlocal-5.2-lightgrey)
![urllib3](https://img.shields.io/badge/urllib3-2.2.2-blue)

- **Raspberry Pi**: 저렴하고 강력한 싱글 보드 컴퓨터
- **RPi.GPIO**: Raspberry Pi의 GPIO 핀을 쉽게 제어할 수 있게 해주는 라이브러리
- **MFRC522**: RFID/NFC 리더 모듈을 다루기 위한 라이브러리로, 카드 인식 및 데이터 전송 기능을 제공

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
