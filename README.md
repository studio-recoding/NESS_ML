# NESS_ML

NESS 프로젝트의 ML 레포지토리입니다.

## 🪧 About source code

NESS_ML의 프로젝트 구조는 다음과 같습니다.

```
NESS_ML
├─ app
│  ├─ database
│  │  ├─ chroma_db.py
│  │  └─ connect_rds.py
│  ├─ dto
│  │  ├─ db_dto.py
│  │  └─ openai_dto.py
│  ├─ main.py
│  ├─ prompt
│  │  ├─ email_prompt.py
│  │  ├─ openai_config.ini
│  │  ├─ openai_prompt.py
│  │  ├─ persona_prompt.py
│  │  └─ report_prompt.py
│  ├─ routers
│  │  ├─ chat.py
│  │  ├─ chromadb.py
│  │  ├─ email.py
│  │  ├─ recommendation.py
│  │  ├─ report.py
│  │  └─ __init__.py
│  └─ __init__.py
├─ Dockerfile
├─ README.md
└─ requirements.txt

```

`database`: vector db인 `chroma`와의 연결을 관리합니다. 또한 필요할 경우 rds에서 정보를 가져옵니다.

`dto`: request 및 response dto를 정의합니다.

`main`: 서버의 main 실행 파일입니다. api 엔드포인트는 router를 통해 관리됩니다.

`prompt`: open ai api 호출 시 사용하는 prompt를 관리합니다.

`routers`: api 엔드포인트입니다.

## 👩‍💻 Prerequisites
NESS의 백엔드 서버는 `FASTAPI`  애플리케이션으로, `requirements.txt`에 적힌 라이브러리 설치가 사전에 이루어져야 합니다.
```bash
pip install -r requirements.txt
```

## 🔧 How to build
이 레포지토리는 해당 명령어로 Clone 가능합니다.
```bash
https://github.com/studio-recoding/NESS_ML.git
```
별도의 빌드는 필요하지 않습니다.

##  🚀 How to run
다음 명령어로 `8080` 포트에서 실행 가능합니다.
```bash
uvicorn main:app -reload
```
## ✅ How to test
NESS의 ML 서버는 다음과 같은 프로그램을 통해서 API를 테스트할 수 있습니다.
`http://localhost:8080/API엔드포인트`로 API를 호출하면 동작을 확인할 수 있습니다.
- POSTMAN

## 📌 Description of used open source
NESS의 ML 서버는 다음과 같은 오픈 소스를 사용하고 있습니다.
<div>
<img alt="FastAPI" src ="https://img.shields.io/badge/fastapi-009688.svg?&style=for-the-badge&logo=fastapi&logoColor=white"/>
</div>

