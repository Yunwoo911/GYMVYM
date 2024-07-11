import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

class Databases():
    # PostgreSQL 데이터베이스 연결 설정
    def __init__(self):
        self.db = psycopg2.connect(host= os.getenv('DATABASE_HOST'),  
                                    dbname= os.getenv('DATABASE_NAME'),
                                    user= os.getenv('DATABASE_USER'), 
                                    password= os.getenv('DATABASE_PASSWORD'), 
                                    port= os.getenv('DATABASE_PORT'))
        self.cursor = self.db.cursor()

    def __del__(self):
        # 객체가 소멸될 때 데이터베이스 연결을 닫음
        self.db.close()
        self.cursor.close()

    def execute(self,query,args={}):
        # 쿼리를 실행하고 결과를 반환
        self.cursor.execute(query,args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        # 트랜잭션 커밋
        self.cursor.commit()

# CRUD 클래스는 Databases 클래스를 상속받음
class CRUD(Databases):
    def createDB(self, nfc_uid):
        sql = "" \
        .format(nfc_uid=nfc_uid)
        try:
            # SQL 쿼리 실행
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e:
            # 오류 발생 시 결과에 오류 메시지 저장
            result = ("데이터베이스 쓰기 오류:", e)

    # (Read) select 읽기/찾기
    def readDB(self, name):
        sql = "SELECT username, nfc_uid, phone_number, email  \
            FROM public.account_customuser where username='{name}'"  \
            .format(name=name)
        try:
            # SQL 쿼리 실행
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e:
            # 오류 발생 시 결과에 오류 메시지 저장
            result = ("데이터베이스 읽기 오류:", e)
        
        return result

    # Update 변경
    def updateDB(self, nfc_uid, username):
        sql = "UPDATE public.account_customuser SET nfc_uid='{nfc_uid}' WHERE username ='{username}'" \
        .format(nfc_uid=nfc_uid, username=username)
        try:
            # SQL 쿼리 실행 및 커밋
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            # 오류 발생 시 메시지 출력
            print("데이터베이스 업데이트 오류:", e)

    # 삭제/제거
    def deleteDB(self, condition):
        sql = "DELETE FROM public.account_customuser WHERE {condition};" \
            .format(condition=condition)
        try:
            # SQL 쿼리 실행 및 커밋
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            # 오류 발생 시 메시지 출력
            print("데이터베이스 삭제 오류:", e)