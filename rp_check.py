import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import tkinter as tk

reader = SimpleMFRC522()
global_id = ''

def add_to_list(): #카드 등록
    card_info = entry.get()
    with open("list.txt", 'a') as file:
        file.write('\n')
        file.write(card_info)
        file.write('\n')
        file.write(global_id)

def check_attendance(): #목록일어서 카드가 목록에 있다면 출석체크기록 작성
    with open("list.txt", 'r') as file:
        lines = file.readlines()
        
    current_date = time.strftime('%c', time.localtime(time.time()))

    with open("attendance_record.txt", 'a') as file:
        for i in range(0, len(lines), 2):
            if global_id == lines[i]:
                file.write('\n')
                file.write(lines[i-1])
                file.write(' 출석 ')
                file.write(current_date)

                attendance_record = (lines[i-1], '출석', current_date)
                print(attendance_record)

try:
    while True:
        id, text = reader.read()
        print(f'{id:#x}')
        global_id = format(id)

        root = tk.Tk()
        root.title("출석체크")
        root.geometry("640x400+100+100")

        # GUI 요소 생성
        entry = tk.Entry(root)
        entry.grid(row=2, column=1)

        label = tk.Label(root, text='*출석체크*')
        label.grid(row=0, column=1)

        add_button = tk.Button(root, text='목록 추가', command=add_to_list)
        add_button.grid(row=1, column=1)

        check_button = tk.Button(root, text='출석', command=check_attendance)
        check_button.grid(row=3, column=1)

        with open("list.txt", 'r') as file:
            lines = file.readlines()

        list_content = ''.join(lines[1:])
        print(list_content)

        list_label = tk.Label(root, text=list_content)
        list_label.grid(row=2, column=2)

        root.mainloop()

finally:
    GPIO.cleanup()
