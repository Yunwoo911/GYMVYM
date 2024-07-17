import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

reader = SimpleMFRC522()

def read_with_timeout(timeout=1):
    start_time = time.time()
    while True:
        id, text = reader.read_no_block()
        if id is not None:
            return id, text
        if time.time() - start_time > timeout:
            return None, None
        time.sleep(0.1)  # 짧은 딜레이

def add_to_list():
    try:
        id, text = read_with_timeout(timeout=5)  # timeout을 5초로 설정
        if id is not None:
            with open("list.txt", 'a') as file:
                file.write('\n')
                file.write(str(id))  # id를 문자열로 변환하여 저장
            print("{0}".format(id))
        else:
            print("Timeout: NFC 카드를 인식할 수 없습니다.")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    add_to_list()
