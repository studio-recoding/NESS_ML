import configparser
import os

from dotenv import load_dotenv
from fastapi import APIRouter
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from app.prompt import openai_prompt

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

@router.get("/main")
def get_recommendation():

    # 모델
    chat_model = ChatOpenAI(temperature=0,  # 창의성 (0.0 ~ 2.0)
                            max_tokens=2048,  # 최대 토큰수
                            model_name='gpt-3.5-turbo-1106',  # 모델명
                            openai_api_key=OPENAI_API_KEY  # API 키
                            )


    # 템플릿
    recommendation_template = openai_prompt.Template.recommendation_template

    prompt = PromptTemplate.from_template(recommendation_template)
    return chat_model.predict(prompt.format())