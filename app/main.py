# SERVER
import uvicorn
from dotenv import load_dotenv

# BACKEND
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
import asyncio

# VECTOR DB Module
import app.database.chroma_db as vectordb

# AI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# DTO
from app.dto import openai_dto
from app.prompt import openai_prompt
from app.dto.db_dto import AddScheduleDTO

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

@app.post("/add_schedule/")
async def add_schedule_endpoint(schedule_data: AddScheduleDTO):
    try:
        # vectordb.add_db_data 함수를 비동기적으로 호출합니다.
        await vectordb.add_db_data(schedule_data)
        return {"message": "Schedule added successfully"}
    except Exception as e:
        # 에러 처리: 에러가 발생하면 HTTP 500 응답을 반환합니다.
        raise HTTPException(status_code=500, detail=str(e))
# 한 줄 추천
@app.get("/main/recommendation")
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


@app.get("/chatgpt/langchain/case")
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
    case = chat_model.predict(prompt.format(question=question))

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
#@app.post("/chatgpt/langchain/normal") # 테스트용 엔드포인트
async def get_langchain_normal(data: openai_dto.PromptRequest): # case 1 : normal
    print("running case 1")
    # description: use langchain
    chat_model = ChatOpenAI(temperature=0,  # 창의성 (0.0 ~ 2.0)
                            max_tokens=2048,  # 최대 토큰수
                            model_name='gpt-3.5-turbo-1106',  # 모델명
                            openai_api_key=OPENAI_API_KEY  # API 키
                            )
    question = data.prompt
    # 기존 모델 문제 생김
    # chat_model = LangchainOpenAI(openai_api_key=OPENAI_API_KEY)

    # description: give NESS's ideal instruction as template
    my_template = openai_prompt.Template.case1_template

    prompt = PromptTemplate.from_template(my_template)
    return chat_model.predict(prompt.format(output_language="Korean", question=question))

# case 2 : 일정 생성
#@app.post("/chatgpt/langchain/make_schedule") # 테스트용 엔드포인트
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
    return chat_model.predict(prompt.format(output_language="Korean", question=question))

# case 3 : rag
#@app.post("/chatgpt/langchain/rag") # 테스트용 엔드포인트
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
    response = chat_model.predict(prompt.format(output_language="Korean", question=question, schedule=schedule))
    print(response)
    return response


if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", port=8000, app=app)
