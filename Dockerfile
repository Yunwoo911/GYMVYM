# 베이스 이미지 선택 (Python 3.8 사용)
FROM python:3.10-slim

# 환경 변수 설정
ENV PYTHONUNBUFFERED 1

# 작업 디렉토리 생성
WORKDIR /app

# 필요 패키지 설치를 위해 시스템 패키지 업데이트 및 설치
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev \
    && apt-get clean

# 요구사항 파일을 복사하고 필요 패키지 설치
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 소스 코드를 컨테이너로 복사
COPY . /app/

# 포트 노출 (Django 기본 포트)
EXPOSE 8000

# 명령어 설정 (Django 개발 서버 실행)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
