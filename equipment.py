import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
from add_DB import CRUD

reader = SimpleMFRC522()

equipment_id = '1' #내 RFID가 1이라고 가정

