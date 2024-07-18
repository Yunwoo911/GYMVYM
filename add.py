import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
from add_DB import CRUD

reader = SimpleMFRC522()
db = CRUD()  # CRUD 객체 생성

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

# NFC 카드를 읽고, 읽은 ID와 사용자 입력 username을 데이터베이스에 저장
def add_to_database():
    try:
        id, _ = read_with_timeout(timeout=5)
        if id is not None:
            # 사용자의 username 입력 받기
            username = input("등록하실 분의 이름을 적어주세요: ")
            
            # 데이터베이스에서 username 조회
            user_data = db.readDB(username)
            
            if not user_data:
                print("없는 회원입니다.")
            else:
                # 데이터베이스에서 nfc_uid 조회
                nfc_data = db.read_by_nfc_uid(str(id))
                
                if nfc_data:
                    print("이미 존재하는 NFC ID입니다.")
                else:
                    # 데이터베이스에 NFC ID와 사용자 입력 username 저장
                    db.updateNFC(nfc_uid=str(id), username=username)
                    print("NFC ID {} 이(가) 데이터베이스에 저장되었습니다.".format(str(id)))
        else:
            print("Timeout: NFC 카드를 인식할 수 없습니다.")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    add_to_database()
