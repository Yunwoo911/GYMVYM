import RPi.GPIO as GPIO
from time import sleep
from PIL import Image, ImageDraw, ImageFont
from mfrc522 import SimpleMFRC522
from luma.core.interface.serial import spi
from luma.oled.device import sh1106

# GPIO 핀 번호 모드 설정
GPIO.setmode(GPIO.BCM)

# OLED 초기화
RST = 24  # OLED의 Reset 핀
DC = 23   # OLED의 Data/Command 핀
CS_OLED = 8  # OLED의 Chip Select 핀 (CE1으로 설정)
SPI_PORT = 0  # SPI 포트 번호
SPI_DEVICE_OLED = 1  # OLED 장치 번호 (CE1)

# SPI 초기화
serial = spi(device=SPI_DEVICE_OLED, port=SPI_PORT, gpio_DC=DC, gpio_RST=RST)
device = sh1106(serial, width=128, height=64, rotate=0)

# 디스플레이 초기화
device.clear()
device.show()

# 이미지 생성 (흑백 모드)
width = device.width
height = device.height
image = Image.new('1', (width, height))

# 이미지에 그리기 위한 객체 생성
draw = ImageDraw.Draw(image)

# 한글 폰트 로드
font_path = "/home/pi/NanumGothic.ttf"  # 폰트 파일 경로
font = ImageFont.truetype(font_path, 14)  # 폰트 크기를 적절히 조절

# RFID 초기화 (SPI 객체 없이 초기화)
reader = SimpleMFRC522()

# RFID 태그를 읽는 함수
def read_rfid():
    try:
        print("RFID 태그를 태그해주세요...")
        uid = reader.read_id()  # UID 읽기
        return uid
    except Exception as e:
        print("RFID 읽기 오류:", e)
        return None

# 텍스트를 OLED에 표시하는 함수
def display_text(text):
    # 이미지 클리어
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    # 텍스트 그리기
    draw.text((0, 0), text, font=font, fill=255)
    # 디스플레이 업데이트
    device.display(image)
    device.show()  # Ensure the display is updated

try:
    while True:
        # RFID 읽기
        uid = read_rfid()
        if uid:
            # UID를 OLED에 표시
            display_text("NFC 태그 감지됨: " + str(uid))
        else:
            # 카드 대기 메시지 표시
            display_text("다시 태그해주세요")
        sleep(3)  # 3초 대기
except KeyboardInterrupt:
    # 프로그램 종료 시 정리
    GPIO.cleanup()
    device.clear()
    device.show()
