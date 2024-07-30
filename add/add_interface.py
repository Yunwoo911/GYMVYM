import tkinter as tk
from tkinter import messagebox
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
from add_DB import CRUD

# RFID 리더와 데이터베이스 객체 생성
reader = SimpleMFRC522()
db = CRUD()

# 메인 애플리케이션 클래스
class RFIDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RFID 등록 시스템")
        self.root.geometry("800x600")  # 윈도우 크기 설정

        # 검색 사용자 이름 입력
        self.label_name = tk.Label(root, text="검색할 사용자의 이름을 입력하세요:")
        self.label_name.pack(pady=10)  # 여백 추가

        self.entry_name = tk.Entry(root, width=50)  # 입력 필드 너비 조정
        self.entry_name.pack(pady=10)

        self.button_search = tk.Button(root, text="검색", command=self.search_user, width=20)  # 버튼 너비 조정
        self.button_search.pack(pady=10)

        # 사용자 목록 및 선택
        self.listbox_users = tk.Listbox(root, width=80, height=20)  # Listbox 크기 조정
        self.listbox_users.pack(pady=10)

        self.button_select = tk.Button(root, text="선택한 사용자 등록", command=self.register_user, width=20)  # 버튼 너비 조정
        self.button_select.pack(pady=10)

        self.label_message = tk.Label(root, text="", wraplength=700)  # 메시지 레이블 너비 조정
        self.label_message.pack(pady=10)

    def search_user(self):
        name = self.entry_name.get()
        if not name:
            messagebox.showwarning("입력 오류", "이름을 입력해 주세요.")
            return
        
        result = db.readDB(name)
        if result:
            self.listbox_users.delete(0, tk.END)
            for user in result:
                self.listbox_users.insert(tk.END, f"{user[0]} | {user[1]} | {user[2]} | {user[3]}")
        else:
            messagebox.showinfo("검색 결과", "사용자를 찾을 수 없습니다.")

    def register_user(self):
        selected_index = self.listbox_users.curselection()
        if not selected_index:
            messagebox.showwarning("선택 오류", "사용자를 선택해 주세요.")
            return
        
        selected_user = self.listbox_users.get(selected_index[0]).split(" | ")
        username = selected_user[0]

        id, _ = self.read_with_timeout(timeout=5)
        if id is not None:
            nfc_data = db.read_by_nfc_uid(str(id))
            if nfc_data:
                messagebox.showwarning("등록 오류", "이미 존재하는 NFC ID입니다.")
            else:
                db.updateNFC(nfc_uid=str(id), username=username)
                messagebox.showinfo("등록 성공", f"NFC ID {id}가 {username}에게 등록되었습니다.")
        else:
            messagebox.showwarning("등록 오류", "NFC 카드를 인식할 수 없습니다.")

    def read_with_timeout(self, timeout=1):
        start_time = time.time()
        while True:
            id, text = reader.read_no_block()
            if id is not None:
                return id, text
            if time.time() - start_time > timeout:
                return None, None
            time.sleep(0.1)

# Tkinter 애플리케이션 실행
if __name__ == "__main__":
    root = tk.Tk()
    app = RFIDApp(root)
    root.mainloop()
