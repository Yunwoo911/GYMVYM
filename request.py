import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests
import time

reader = SimpleMFRC522()

DJANGO_ENDPOINT = ""  # Django 서버의 실제 URL로 변경

def send_to_django(nfc_uid):
    try:
        response = requests.post(DJANGO_ENDPOINT, data={'nfc_uid': nfc_uid})
        if response.status_code == 200:
            print("Django 서버에 NFC UID를 성공적으로 전송했습니다.")
        else:
            print(f"NFC UID 전송에 실패했습니다. 상태 코드: {response.status_code}")
    except requests.RequestException as e:
        print(f"Django에 데이터를 전송하는 중 오류가 발생했습니다: {e}")

try:
    print("리더기 근처에 태그를 가져다 대세요.")
    while True:
        id, text = reader.read()
        print(f"ID: {id}")
        send_to_django(id)
        time.sleep(2)  # 연속 읽기 방지를 위한 대기 시간

except KeyboardInterrupt:
    GPIO.cleanup()
    print("GPIO 정리 완료")
