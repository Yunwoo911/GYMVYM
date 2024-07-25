import os
import time
from luma.core.interface.serial import spi
from luma.oled.device import ssd1306
from PIL import Image

# SPI 초기화
serial = spi(device=1, port=0)  # CS 핀을 1로 설정
device = ssd1306(serial)

# 이미지 로드 및 크기 조정
image_path = '/home/pi/pi-rfid/GYMVYM/sample/logo.png'  # 표시할 이미지 파일 경로
if os.path.exists(image_path):
    image = Image.open(image_path).convert('1')  # 이미지를 흑백으로 변환

    # OLED 해상도에 맞게 이미지 크기 조정
    image = image.resize(device.size)  # ANTIALIAS 제거

    device.display(image)  # OLED에 이미지 표시
else:
    print("이미지 파일이 존재하지 않습니다.")

# 프로그램 종료 전 잠시 대기
time.sleep(5)  # 5초 동안 이미지 표시
