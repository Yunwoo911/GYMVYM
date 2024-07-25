import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
from add.add_DB import CRUD
from machine import Pin, SPI
import ssd1306

# RFID RC522 설정
RFID_CS = 8
RFID_RST = 25
reader = SimpleMFRC522()

# OLED 설정
OLED_CS = 17
OLED_RST = 16
OLED_DC = 20
spi_port = 0
MOSI = 10
CLK = 11

WIDTH = 128
HEIGHT = 64

# SPI 초기화
spi = SPI(spi_port, baudrate=40000000, mosi=Pin(MOSI), sck=Pin(CLK))
oled = ssd1306.SSD1306_SPI(WIDTH, HEIGHT, spi, dc=Pin(OLED_DC), res=Pin(OLED_RST), cs=Pin(OLED_CS), external_vcc=False)

db = CRUD()  # CRUD 객체 생성

def search(name):
    result = db.readDB(name)
    if result:
        print("정보 : ", result)
        return result
    else:
        return None

def read_with_timeout(timeout=1):
    start_time = time.time()
    while True:
        id, text = reader.read_no_block()
        if id is not None:
            return id, text
        if time.time() - start_time > timeout:
            return None, None
        time.sleep(0.1)

def select_user(users):
    print("여러 명의 사용자가 검색되었습니다. 등록할 사용자를 선택하세요.")
    for i, user in enumerate(users):
        print(f"{i}: {user}")
    while True:
        try:
            index = int(input("등록할 사용자의 번호를 입력하세요: "))
            if 0 <= index < len(users):
                return users[index]
            else:
                print("잘못된 번호입니다. 다시 입력해 주세요.")
        except ValueError:
            print("숫자를 입력해 주세요.")

def add_to_database(selected_user):
    try:
        id, _ = read_with_timeout(timeout=5)
        if id is not None:
            nfc_data = db.read_by_nfc_uid(str(id))
            if nfc_data:
                print("이미 존재하는 NFC ID입니다.")
                oled_message("이미 존재하는\nNFC ID입니다.")
            else:
                db.updateNFC(nfc_uid=str(id), username=selected_user[0])
                print("NFC ID {} 이(가) 데이터베이스에 저장되었습니다.".format(str(id)))
                oled_message("NFC ID 저장됨")
        else:
            print("Timeout: NFC 카드를 인식할 수 없습니다.")
            oled_message("Timeout: NFC\n카드를 인식할 수 없음")
    finally:
        GPIO.cleanup()

def oled_message(message):
    oled.fill(0)
    for i, line in enumerate(message.split('\n')):
        oled.text(line, 0, i*10, 1)
    oled.show()

def interface():
    while True:
        name_to_search = input("검색할 사용자의 이름을 입력하세요: ")
        if name_to_search.lower() == 'q':  # 'q'를 입력하면 종료
            print("프로그램을 종료합니다.")
            oled_message("프로그램 종료")
            break
        if not name_to_search:  # 빈칸으로 입력했을 때
            print("이름을 입력해 주세요.")
            oled_message("이름을 입력해\n주세요")
            continue
        users = search(name_to_search)
        if users is None:  # 사용자를 찾을 수 없는 경우
            print("사용자를 찾을 수 없습니다. 다시 시도해 주세요.")
            oled_message("사용자를 찾을 수\n없습니다")
            continue
        if len(users) > 1:
            selected_user = select_user(users)
        else:
            selected_user = users[0]
        print("NFC 카드를 인식해 주세요.")
        oled_message("NFC 카드를\n인식해 주세요")
        new_nfc_uid, _ = read_with_timeout(timeout=5)
        if new_nfc_uid is None:
            print("Timeout: NFC 카드를 인식할 수 없습니다.")
            oled_message("Timeout: NFC\n카드를 인식할 수 없음")
            continue
        add_to_database(selected_user)
        break

if __name__ == "__main__":
    interface()
