import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import tkinter as tk
from threading import Thread

reader = SimpleMFRC522()
global_id = ''

def add_to_list():
    global global_id
    card_info = entry.get()
    with open("list.txt", 'a') as file:
        file.write(global_id + '\n')
        file.write(card_info + '\n')
    print_list()

def check_attendance():
    global global_id
    with open("list.txt", 'r') as file:
        lines = file.readlines()
        
    current_date = time.strftime('%c', time.localtime(time.time()))

    with open("attendance_record.txt", 'a') as file:
        for i in range(0, len(lines), 2):
            if global_id == lines[i].strip():
                file.write(lines[i+1].strip() + ' 출석 ' + current_date + '\n')
                attendance_record = (lines[i+1].strip(), '출석', current_date)
                print(attendance_record)

def read_rfid_and_update_gui():
    global global_id
    while True:
        id, text = reader.read()
        print(f'{id:#x}')
        global_id = str(id)
        root.after(100, print_list)  # 0.1초마다 리스트 갱신

def print_list():
    with open("list.txt", 'r') as file:
        lines = file.readlines()

    list_content = ''.join(lines)
    list_label.config(text=list_content)

def on_closing():
    root.destroy()
    GPIO.cleanup()

root = tk.Tk()
root.title("출석체크")
root.geometry("640x400+100+100")

entry = tk.Entry(root)
entry.grid(row=2, column=1)

label = tk.Label(root, text='*출석체크*')
label.grid(row=0, column=1)

add_button = tk.Button(root, text='목록 추가', command=add_to_list)
add_button.grid(row=1, column=1)

check_button = tk.Button(root, text='출석', command=check_attendance)
check_button.grid(row=3, column=1)

list_label = tk.Label(root, text='')
list_label.grid(row=2, column=2)

# 종료 버튼 추가
exit_button = tk.Button(root, text='종료', command=on_closing)
exit_button.grid(row=4, column=1)

# RFID 리더기 읽기와 GUI 갱신을 별도 스레드에서 실행
rfid_thread = Thread(target=read_rfid_and_update_gui)
rfid_thread.start()

# 메인 루프 시작
root.mainloop()
