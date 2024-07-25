import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests
import time

GYM_ID = 1

reader = SimpleMFRC522()

DJANGO_ENDPOINT = "https://a146-122-34-248-34.ngrok-free.app/visitlogs/nfc_entrance/"  # Django 서버의 실제 URL로 변경

def send_to_django(nfc_uid, gym_id):
    print(f"전송할 NFC UID: {nfc_uid}, gym_id: {gym_id}")  # 디버깅 출력 추가
    try:
        headers = {'Content-Type': 'application/json'}
        data = {'nfc_uid': nfc_uid, 'gym_id': gym_id}  # gym_id를 추가
        response = requests.post(DJANGO_ENDPOINT, json=data, headers=headers)
        print(f"서버 응답 코드: {response.status_code}")  # 디버깅 출력 추가
        if response.status_code == 200:
            print("Django 서버에 NFC UID를 성공적으로 전송했습니다.")
        else:
            print(f"NFC UID 전송에 실패했습니다. 상태 코드: {response.status_code}")
            print(f"서버 응답 내용: {response.text}")  # 서버 응답 내용 추가
    except requests.RequestException as e:
        print(f"Django에 데이터를 전송하는 중 오류가 발생했습니다: {e}")



try:
    print("리더기 근처에 태그를 가져다 대세요.")
    while True:
        id, text = reader.read()
        id_str = str(id)  # NFC UID를 문자열로 변환
        print(f"ID: {id_str}")
        send_to_django(id_str, GYM_ID)  # 문자열로 전송
        time.sleep(2)  # 연속 읽기 방지를 위한 대기 시간

except KeyboardInterrupt:
    GPIO.cleanup()
    print("GPIO 정리 완료")
