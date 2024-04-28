import configparser
import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, status, HTTPException
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from app.dto.db_dto import RecommendationMainRequestDTO
from app.dto.openai_dto import ChatResponse
from app.prompt import openai_prompt
import app.database.chroma_db as vectordb

router = APIRouter(
    prefix="/recommendation",
    tags=["recommendation"]
)

# description: load env variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# description: load config variables from openai_config.ini file
CONFIG_FILE_PATH = "app/prompt/openai_config.ini"
config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)

@router.post("/main", status_code=status.HTTP_200_OK)
async def get_recommendation(user_data: RecommendationMainRequestDTO) -> ChatResponse:
    try:
        # 모델
        config_recommendation = config['NESS_RECOMMENDATION']

        chat_model = ChatOpenAI(temperature=config_recommendation['TEMPERATURE'],  # 창의성 (0.0 ~ 2.0)
                                max_tokens=config_recommendation['MAX_TOKENS'],  # 최대 토큰수
                                model_name=config_recommendation['MODEL_NAME'],  # 모델명
                                openai_api_key=OPENAI_API_KEY  # API 키
                                )

        # vectordb에서 유저의 정보를 가져온다.
        schedule = await vectordb.db_daily_schedule(user_data)

        print(schedule)

        # 템플릿
        recommendation_template = openai_prompt.Template.recommendation_template

        prompt = PromptTemplate.from_template(recommendation_template)
        result = chat_model.predict(prompt.format(output_language="Korean", schedule=schedule))
        print(result)
        return ChatResponse(ness=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))