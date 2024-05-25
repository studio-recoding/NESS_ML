import configparser
import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends, status

from app.dto.db_dto import AddScheduleDTO, DeleteScheduleDTO, UpdateScheduleDTO
from app.database.chroma_db import add_db_data, delete_db_data, update_db_data, get_chroma_client

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


@router.post("/add_schedule", status_code=status.HTTP_201_CREATED)
async def add_schedule_endpoint(schedule_data: AddScheduleDTO, chroma_client=Depends(get_chroma_client)):
    try:
        # 직접 `add_db_data` 함수를 비동기적으로 호출합니다.
        await add_db_data(schedule_data)
        return {"message": "Schedule added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete_schedule", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule_endpoint(schedule_data: DeleteScheduleDTO, chroma_client=Depends(get_chroma_client)):
    try:
        # 직접 `add_db_data` 함수를 비동기적으로 호출합니다.
        await delete_db_data(schedule_data)
        return {"message": "Schedule delete successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update_schedule", status_code=status.HTTP_200_OK)
async def update_schedule_endpoint(schedule_data: UpdateScheduleDTO, chroma_client=Depends(get_chroma_client)):
    try:
        # 데이터베이스 업데이트 함수 호출
        await update_db_data(schedule_data)
        return {"message": "Schedule updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))