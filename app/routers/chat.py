# app/routers/chat.py
import configparser
import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from app.dto import openai_dto
from app.prompt import openai_prompt

import app.database.chroma_db as vectordb

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

# description: load env variables from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# description: load config variables from openai_config.ini file
CONFIG_FILE_PATH = "app/prompt/openai_config.ini"
config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)

@router.post("/case")
async def get_langchain_case(data: openai_dto.PromptRequest):
    # description: use langchain

    config_normal = config['NESS_NORMAL']

    chat_model = ChatOpenAI(temperature=config_normal['TEMPERATURE'],  # 창의성 (0.0 ~ 2.0)
                            max_tokens=config_normal['MAX_TOKENS'],  # 최대 토큰수
                            model_name=config_normal['MODEL_NAME'],  # 모델명
                            openai_api_key=OPENAI_API_KEY  # API 키
                            )
    question = data.prompt

    # description: give NESS's instruction as for case analysis
    my_template = openai_prompt.Template.case_classify_template

    prompt = PromptTemplate.from_template(my_template)
    case = await chat_model.predict(prompt.format(question=question))

    print(case)
    case = int(case)
    if case == 1:
        return await get_langchain_normal(data)

    elif case == 2:
        return await get_langchain_schedule(data)

    elif case == 3:
        return await get_langchain_rag(data)

    else:
        print("wrong case classification")
        # 적절한 HTTP 상태 코드와 함께 오류 메시지를 반환하거나, 다른 처리를 할 수 있습니다.
        raise HTTPException(status_code=400, detail="Wrong case classification")


# case 1 : normal
#@router.post("/case/normal") # 테스트용 엔드포인트
async def get_langchain_normal(data: openai_dto.PromptRequest): # case 1 : normal
    print("running case 1")
    # description: use langchain
    chat_model = ChatOpenAI(temperature=0,  # 창의성 (0.0 ~ 2.0)
                            max_tokens=2048,  # 최대 토큰수
                            model_name='gpt-3.5-turbo-1106',  # 모델명
                            openai_api_key=OPENAI_API_KEY  # API 키
                            )
    question = data.prompt

    # description: give NESS's ideal instruction as template
    my_template = openai_prompt.Template.case1_template

    prompt = PromptTemplate.from_template(my_template)
    response = await chat_model.predict(prompt.format(output_language="Korean", question=question))
    print(response)
    return response

# case 2 : 일정 생성
#@router.post("/case/make_schedule") # 테스트용 엔드포인트
async def get_langchain_schedule(data: openai_dto.PromptRequest):
    print("running case 2")
    # description: use langchain
    chat_model = ChatOpenAI(temperature=0,  # 창의성 (0.0 ~ 2.0)
                            max_tokens=2048,  # 최대 토큰수
                            model_name='gpt-3.5-turbo-1106',  # 모델명
                            openai_api_key=OPENAI_API_KEY  # API 키
                            )
    question = data.prompt
    case2_template = openai_prompt.Template.case2_template

    prompt = PromptTemplate.from_template(case2_template)
    response = await chat_model.predict(prompt.format(output_language="Korean", question=question))
    print(response)
    return response

# case 3 : rag
#@router.post("/case/rag") # 테스트용 엔드포인트
async def get_langchain_rag(data: openai_dto.PromptRequest):
    print("running case 3")
    # description: use langchain
    chat_model = ChatOpenAI(temperature=0,  # 창의성 (0.0 ~ 2.0)
                            max_tokens=2048,  # 최대 토큰수
                            model_name='gpt-3.5-turbo-1106',  # 모델명
                            openai_api_key=OPENAI_API_KEY  # API 키
                            )
    question = data.prompt

    # vectordb.search_db_query를 비동기적으로 호출합니다.
    schedule = await vectordb.search_db_query(question)  # vector db에서 검색

    # description: give NESS's ideal instruction as template
    case3_template = openai_prompt.Template.case3_template

    prompt = PromptTemplate.from_template(case3_template)
    # 여기서는 chat_model.predict가 비동기 함수인지, 동기 함수인지에 따라 처리가 달라질 수 있습니다.
    # 만약 비동기 함수라면 await를 사용해야 합니다. 아래 코드는 동기 함수를 가정하고 작성되었습니다.
    # 비동기 함수라면, 예: response = await chat_model.predict(...) 형태로 수정해야 합니다.
    response = await chat_model.predict(prompt.format(output_language="Korean", question=question, schedule=schedule))
    print(response)
    return response
