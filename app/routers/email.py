import configparser
import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, status, HTTPException
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from app.dto.db_dto import EmailRequestDTO
from app.dto.openai_dto import EmailResponse
from app.prompt import email_prompt, persona_prompt
import app.database.chroma_db as vectordb

router = APIRouter(
    prefix="/email",
    tags=["email"]
)

# description: load env variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# description: load config variables from openai_config.ini file
CONFIG_FILE_PATH = "app/prompt/openai_config.ini"
config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)

# description: 유저의 하루 스케줄을 기반으로 이메일 내용을 작성한다.
@router.post("/daily", status_code=status.HTTP_200_OK)
async def get_daily_email(user_data: EmailRequestDTO) -> EmailResponse:
    try:
        # 모델
        config_recommendation = config['NESS_EMAIL']

        chat_model = ChatOpenAI(temperature=config_recommendation['TEMPERATURE'],  # 창의성 (0.0 ~ 2.0)
                                max_tokens=config_recommendation['MAX_TOKENS'],  # 최대 토큰수
                                model_name=config_recommendation['MODEL_NAME'],  # 모델명
                                openai_api_key=OPENAI_API_KEY  # API 키
                                )

        # vectordb에서 유저의 정보를 가져온다.
        schedule = await vectordb.db_daily_schedule(user_data)

        print(schedule)

        # 템플릿
        email_template = email_prompt.Template.daily_email_template
        
        # 페르소나 추후 사용 가능
        # persona = user_data.user_persona
        # user_persona_prompt = persona_prompt.Template.from_persona(persona)

        # 이메일 내용
        prompt = PromptTemplate.from_template(email_template)
        email_text = chat_model.predict(
            prompt.format(output_language="Korean", schedule=schedule))
        print(email_text)

        # 이메일에 들어갈 텍스트
        image_url = "달리를 이용하여 생성할 이미지의 링크"

        return EmailResponse(text=email_text, image=image_url)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))