import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
from add_DB import CRUD

reader = SimpleMFRC522()
db = CRUD()  # CRUD 객체 생성

# 이름으로 검색 : DB에서 이름으로 사용자 정보를 검색
# 입력으로 받은 name 파라미터를 사용하여 DB에서 정보를 읽어옵니다.
# 읽어온 정보를 print로 출력하고, 해당 정보를 반환합니다.
def search(name):
    result = db.readDB(name)
    print("정보 : ", result)
    return result


# NFC 카드를 읽는 기능
# timeout 파라미터는 카드 읽기 시간 제한을 설정하는 값입니다. (기본값:1초)
# reader.read_no_block() 함수를 호출하여 카드 ID와 텍스트 데이터를 읽습니다.
# 카드 ID와 텍스트 데이터가 있으면 해당 값을 반환합니다.
# 지정된 timeout 시간 동안 카드 데이터를 읽지 못하면 None, None을 반환합니다.
# 0.1초 간격으로 반복하여 카드 데이터를 읽습니다.
def read_with_timeout(timeout=1):
    start_time = time.time()
    while True:
        id, text = reader.read_no_block()
        if id is not None:
            return id, text
        if time.time() - start_time > timeout:
            return None, None
        time.sleep(0.1)

# 동명이인이 있을 경우 사용자가 등록할 사용자를 선택
# users 파라미터는 검색된 사용자 목록입니다.
# 검색된 사용자 목록을 출력하고, 사용자가 등록할 사용자의 번호를 입력받습니다.
# 입력받은 번호에 해당하는 사용자 정보를 반환합니다
def select_user(users):
    print("여러 명의 사용자가 검색되었습니다. 등록할 사용자를 선택하세요.")
    for i, user in enumerate(users):
        print(f"{i}: {user}")
    index = int(input("등록할 사용자의 번호를 입력하세요: "))
    selected_user = users[index]
    return selected_user

# NFC 카드를 읽고, 읽은 ID와 사용자 입력 username을 데이터베이스에 저장
# read_with_timeout() 함수를 호출하여 NFC 카드의 ID를 읽습니다.
# 사용자 이름을 데이터베이스에서 조회합니다.
# 데이터베이스에서 해당 NFC 카드 ID가 이미 존재하는지 확인합니다.
# 존재하지 않으면 데이터베이스에 NFC 카드 ID와 사용자 이름을 저장합니다.
# 저장이 완료되면 "NFC ID {ID} 이(가) 데이터베이스에 저장되었습니다." 메시지를 출력합니다.
# 타임아웃이 발생하면 "Timeout: NFC 카드를 인식할 수 없습니다." 메시지를 출력합니다.
def add_to_database(users):
    try:
        id, _ = read_with_timeout(timeout=5)
        if users is not None:
            # 데이터베이스에서 username 조회
            if users:
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
# 사용자로부터 검색할 사용자의 이름을 입력받습니다.
# search() 함수를 호출하여 입력받은 이름으로 데이터베이스에서 사용자 정보를 검색합니다.
# 검색된 사용자 정보가 없으면 다시 입력받도록 합니다.
# 검색된 사용자 정보가 있으면 NFC 카드를 인식하도록 합니다.
# read_with_timeout() 함수를 호출하여 NFC 카드의 ID를 읽습니다.
# NFC 카드 ID가 읽혔으면 add_to_database() 함수를 호출하여 데이터베이스에 저장합니다.
# 이 과정을 무한 반복하며, 사용자가 종료할 때까지 계속 실행됩니다.
def interface():
    while True:
        name_to_search = input("검색할 사용자의 이름을 입력하세요: ")
        if not name_to_search: # 빈칸으로 입력했을 때
            print("이름을 입력해 주세요.")
            continue
        #users = search(name_to_search)
        elif not name_to_search: # 이름이 틀렸을 때
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
