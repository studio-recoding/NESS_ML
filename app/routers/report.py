import configparser
import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, status, HTTPException
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from app.dto.db_dto import ReportMemoryEmojiRequestDTO, ReportTagsRequestDTO
from app.dto.openai_dto import ChatResponse, TagsResponse, TagDescription
from app.prompt import report_prompt, persona_prompt
import app.database.chroma_db as vectordb

router = APIRouter(
    prefix="/report",
    tags=["report"]
)

# description: load env variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# description: load config variables from openai_config.ini file
CONFIG_FILE_PATH = "app/prompt/openai_config.ini"
config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)

@router.post("/memory_emoji", status_code=status.HTTP_200_OK)
async def get_memory_emoji(user_data: ReportMemoryEmojiRequestDTO) -> ChatResponse:
    try:
        # 모델
        config_report_emoji = config['NESS_RECOMMENDATION']

        chat_model = ChatOpenAI(temperature=config_report_emoji['TEMPERATURE'],  # 창의성 (0.0 ~ 2.0)
                                max_tokens=config_report_emoji['MAX_TOKENS'],  # 최대 토큰수
                                model_name=config_report_emoji['MODEL_NAME'],  # 모델명
                                openai_api_key=OPENAI_API_KEY  # API 키
                                )

        # vectordb에서 유저의 정보를 가져온다.
        schedule = await vectordb.db_daily_schedule(user_data)

        print(schedule)

        # 템플릿
        memory_emoji_template = report_prompt.Template.memory_emoji_template

        prompt = PromptTemplate.from_template(memory_emoji_template)
        result = chat_model.predict(prompt.format(output_language="Korean", schedule=schedule))
        print(result)
        return ChatResponse(ness=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tags", status_code=status.HTTP_200_OK)
async def get_tags(user_data: ReportTagsRequestDTO) -> TagsResponse:
    try:
        # 모델
        config_tags = config['NESS_TAGS']

        chat_model = ChatOpenAI(temperature=config_tags['TEMPERATURE'],  # 창의성 (0.0 ~ 2.0)
                                max_tokens=config_tags['MAX_TOKENS'],  # 최대 토큰수
                                model_name=config_tags['MODEL_NAME'],  # 모델명
                                openai_api_key=OPENAI_API_KEY  # API 키
                                )

        # vectordb에서 유저의 정보를 가져온다.
        schedule = await vectordb.db_monthly_tag_schedule(user_data)

        print(schedule)

        # 템플릿
        report_tags_template = report_prompt.Template.report_tags_template
        persona = user_data.user_persona
        user_persona_prompt = persona_prompt.Template.from_persona(persona)

        prompt = PromptTemplate.from_template(report_tags_template)
        result = chat_model.predict(prompt.format(persona=user_persona_prompt, output_language="Korean", schedule=schedule))
        print(result)
        
        # 문자열 파싱해서 dto로 매핑
        tag_entries = result.split("[start]")[1].split("||")
        tags = []

        for entry in tag_entries:
            # ':'를 기준으로 태그와 설명을 분리
            tag, desc = entry.split(": ")
            tags.append(TagDescription(tag=tag.strip(), desc=desc.strip()))

        return TagsResponse(tagList=tags)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))