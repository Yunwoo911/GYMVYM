import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
from add_DB import CRUD

reader = SimpleMFRC522()
db = CRUD()  # CRUD 객체 생성

# 이름으로 검색
def search(name):
    result = db.readDB(name)
    print("정보 : ", result)
    return result

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

# 이름으로 사용자 선택
def select_user(users):
    print("여러 명의 사용자가 검색되었습니다. 업데이트할 사용자를 선택하세요.")
    for i, user in enumerate(users):
        print(f"{i}: {user}")
    index = int(input("업데이트할 사용자의 인덱스를 입력하세요: "))
    selected_user = users[index]
    return selected_user

# NFC 카드를 읽고, 읽은 ID와 사용자 입력 username을 데이터베이스에 저장
def add_to_database():
    try:
        id, _ = read_with_timeout(timeout=5)
        if id is not None:
            # 데이터베이스에서 username 조회
            users = search(str(id))
            if not users:
                print("없는 회원입니다.")
            else:
                # 여러 명의 사용자가 검색되면 선택
                if len(users) > 1:
                    selected_user = select_user(users)
                else:
                    selected_user = users[0]

                # 데이터베이스에서 nfc_uid 조회
                nfc_data = db.read_by_nfc_uid(str(id))
                if nfc_data:
                    print("이미 존재하는 NFC ID입니다.")
                else:
                    # 데이터베이스에 NFC ID와 사용자 입력 username 저장
                    db.updateNFC(nfc_uid=str(id), username=selected_user[0])
                    print("NFC ID {} 이(가) 데이터베이스에 저장되었습니다.".format(str(id)))
        else:
            print("Timeout: NFC 카드를 인식할 수 없습니다.")
    finally:
        GPIO.cleanup()

# 인터페이스 함수
def interface():
    while True:
        name_to_search = input("검색할 사용자의 이름을 입력하세요: ")
        if not name_to_search: # 빈칸으로 입력했을 때
            print("이름을 입력해 주세요.")
            continue
        users = search(name_to_search)
        
        if not users: # 이름이 틀렸을 때
            print("사용자를 찾을 수 없습니다. 다시 시도해 주세요.")
            continue
        
        print("NFC 카드를 인식해 주세요.")
        new_nfc_uid, _ = read_with_timeout(timeout=5)
        if new_nfc_uid is None:
            print("Timeout: NFC 카드를 인식할 수 없습니다.")
            continue
        
        if add_to_database():
            break

if __name__ == "__main__":
    interface()
