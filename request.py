import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests
import time

reader = SimpleMFRC522()

DJANGO_ENDPOINT = "http://your-django-server.com/api/nfc_entrance/"  # Django 서버의 실제 URL로 변경해야 합니다

def send_to_django(nfc_uid):
    try:
        response = requests.post(DJANGO_ENDPOINT, data={'nfc_uid': nfc_uid})
        if response.status_code == 200:
            print("Successfully sent NFC UID to Django server")
        else:
            print(f"Failed to send NFC UID. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred while sending data to Django: {e}")

try:
    print("Hold a tag near the reader")
    while True:
        id, text = reader.read()
        print(f"ID: {id}")
        send_to_django(id)
        time.sleep(2)  # 연속 읽기 방지를 위한 대기 시간

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Cleaned up GPIO")