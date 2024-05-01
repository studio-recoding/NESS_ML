# SERVER
import uvicorn
from dotenv import load_dotenv

# BACKEND
from fastapi import FastAPI, Depends

# ETC
import os
from starlette.middleware.cors import CORSMiddleware
import configparser

# description: load env variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# description: load config variables from openai_config.ini file
CONFIG_FILE_PATH = "prompt/openai_config.ini"
config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)

# FAST API 인스턴스 생성
app = FastAPI()

# 모듈화를 위해 router 사용
from app.routers import chat
app.include_router(chat.router)

from app.routers import chromadb
app.include_router(chromadb.router)

from app.routers import recommendation
app.include_router(recommendation.router)

from app.routers import report
app.include_router(report.router)

from app.routers import email
app.include_router(email.router)

# description: prevent CORS error
origins = [
    "*",
    "http://localhost:8000",
    "https://chat.openai.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", port=8000, app=app)
