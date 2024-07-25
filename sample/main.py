from add.add_DB import CRUD

# CRUD 객체 생성
db = CRUD()

# 이름으로 검색
def search(name):
    result = db.readDB(name)
    print("데이터:", result)
    return result

# 이름을 검색하여 NFC_UID를 수정
def nfc_registration(name, nfc_uid):
    users = search(name)
    if not users:
        return False
    if len(users) > 1:
        print("여러 명의 사용자가 검색되었습니다. 업데이트할 사용자를 선택하세요.")
        for i, user in enumerate(users):
            print(f"{i}: {user}")
        index = int(input("업데이트할 사용자의 인덱스를 입력하세요: "))
        selected_user = users[index]
    elif len(users) == 1:
        selected_user = users[0]

    username = selected_user[0]  # assuming the first column is username
    print("데이터 업데이트 완료")

# 데이터베이스에서 조건에 맞는 데이터 삭제
def delete_data(condition):
    db.deleteDB(condition)
    print("데이터 삭제 완료")

# 인터페이스
def interface():
    while True:
        name_to_search = input("검색할 사용자의 이름을 입력하세요: ")
        if not name_to_search: # 빈칸으로 입력 했을 때
            print("이름을 입력해 주세요.")
            continue
        users = search(name_to_search)
        
        if not users: # 이름이 틀렸을 때
            print("사용자를 찾을 수 없습니다. 다시 시도해 주세요.")
            continue
        
        new_nfc_uid = input("새로운 NFC UID를 입력하세요: ")
        
        if not new_nfc_uid: # 빈칸으로 입력 했을 때
            print("NFC UID를 입력해 주세요.")
            continue
        if nfc_registration(name_to_search, new_nfc_uid):
            break


interface()