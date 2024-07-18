import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
from equip_DB import CRUD

reader = SimpleMFRC522()
db = CRUD()  # CRUD 객체 생성

equipment_id = '1' #내 RFID가 1이라고 가정

# NFC 카드를 읽는 기능
def read_with_timeout(timeout=1):
    start_time = time.time()
    while True:
        id, text = reader.read_no_block()
        if id is not None:
            return id, text
        if time.time() - start_time > timeout:
            return None, None
        time.sleep(0.1)

# NFC 카드를 읽고, 읽은 ID와 시작시간 저장.
def add_to_database():
    try:
        id, _ = read_with_timeout(timeout=5)
        if id is not None:
                # 데이터베이스에서 nfc_uid 조회
                nfc_data = db.read_by_nfc_uid(str(id))
                if nfc_data:
                    print("이미 존재하는 NFC ID입니다.")
                else:
                    # 데이터베이스에 NFC ID와 사용자 입력 username 저장
                    db.updateNFC()
                    print("NFC ID {} 이(가) 데이터베이스에 저장되었습니다.".format(str(id)))
        else:
            print("Timeout: NFC 카드를 인식할 수 없습니다.")
    finally:
        GPIO.cleanup()

# 인터페이스 함수
def interface():
    while True:       
        new_nfc_uid = input("새로운 NFC UID를 입력하세요: ")
        if not new_nfc_uid: # 빈칸으로 입력했을 때
            print("NFC UID를 입력해 주세요.")
            continue
        if add_to_database():
            break

if __name__ == "__main__":
    interface()
