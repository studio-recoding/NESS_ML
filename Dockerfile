# Python 이미지를 기반으로 설정
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# 환경변수 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# 나의 python 버전
FROM python:3.11.1

# /code 폴더 만들기
WORKDIR /code

# ./requirements.txt 를 /code/requirements.txt 로 복사
COPY ./requirements.txt /code/requirements.txt

# requirements.txt 를 보고 모듈 전체 설치(-r)
RUN pip install --no-cache-dir -r /code/requirements.txt

# 이제 app 에 있는 파일들을 /code/app 에 복사
COPY ./app /code/app

# 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]