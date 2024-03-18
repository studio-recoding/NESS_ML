import configparser
import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

from app.dto.db_dto import AddScheduleDTO

router = APIRouter(
    prefix="/chromadb",
    tags=["chromadb"]
)

# description: load env variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# description: load config variables from openai_config.ini file
CONFIG_FILE_PATH = "app/prompt/openai_config.ini"
config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)


@router.post("/add_schedule")
async def add_schedule_endpoint(schedule_data: AddScheduleDTO, vectordb=None):
    try:
        # vectordb.add_db_data 함수를 비동기적으로 호출합니다.
        await vectordb.add_db_data(schedule_data)
        return {"message": "Schedule added successfully"}
    except Exception as e:
        # 에러 처리: 에러가 발생하면 HTTP 500 응답을 반환합니다.
        raise HTTPException(status_code=500, detail=str(e))