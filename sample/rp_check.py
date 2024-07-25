import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import json

# RFID 리더기 객체 생성
reader = SimpleMFRC522()
# 현재 읽은 RFID 카드의 ID를 저장할 변수
global_id = ''

# RFID 카드 정보를 JSON 파일에 추가하는 함수
def add_to_list():
    global global_id
    # 사용자로부터 카드 정보 입력 받기
    card_info = input("카드 정보를 입력하세요: ")
    
    # JSON 파일 읽기
    try:
        with open("list.json", 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    
    # RFID 카드 ID와 카드 정보 추가하기
    data[global_id] = card_info
    
    # JSON 파일에 데이터 저장하기
    with open("list.json", 'w') as file:
        json.dump(data, file, indent=4)
    
    # 파일에 추가된 내용 출력하기
    print_list()

# 출석 체크 기능을 수행하는 함수
def check_attendance():
    global global_id
    
    # JSON 파일 읽기
    try:
        with open("list.json", 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    
    # 현재 날짜와 시간 가져오기
    current_date = time.strftime('%c', time.localtime(time.time()))
    
    # attendance_record.json 파일에 출석 기록 추가하기
    try:
        with open("attendance_record.json", 'r') as file:
            attendance_data = json.load(file)
    except FileNotFoundError:
        attendance_data = {}
    
    if global_id in data:
        attendance_data[data[global_id]] = {'status': '출석', 'date': current_date}
        with open("attendance_record.json", 'w') as file:
            json.dump(attendance_data, file, indent=4)
        attendance_record = (data[global_id], '출석', current_date)
        print(attendance_record)

# RFID 카드를 읽고 global_id 변수에 저장하는 함수
def read_rfid_and_update():
    global global_id
    while True:
        id, text = reader.read()
        print(f'{id:#x}')
        global_id = str(id)

# list.json 파일의 내용을 출력하는 함수
def print_list():
    try:
        with open("list.json", 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    
    print(json.dumps(data, indent=4))

# 메인 함수
def main():
    while True:
        # RFID 카드 읽기 및 global_id 변수 업데이트
        read_rfid_and_update()
        # 사용자 입력에 따라 기능 선택
        option = input("1. 목록 추가, 2. 출석 체크, 3. 종료: ")
        if option == '1':
            add_to_list()
        elif option == '2':
            check_attendance()
        elif option == '3':
            break
        else:
            print("잘못된 입력입니다.")

    # GPIO 정리
    GPIO.cleanup()

if __name__ == "__main__":
    main()
