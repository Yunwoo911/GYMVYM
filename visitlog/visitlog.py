import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
from visitlog.visit_DB import CRUD

reader = SimpleMFRC522()
db = CRUD()  # CRUD 객체 생성