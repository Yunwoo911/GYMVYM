import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

def add_to_list(): #카드 등록
    id, text = reader.read()
    with open("list.txt", 'a') as file:
        file.write('\n')
        file.write(id)
        file.write(text)
