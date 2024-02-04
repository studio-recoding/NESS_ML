# SERVER
import uvicorn
from dotenv import load_dotenv

# BACKEND
from fastapi import FastAPI

# VECTOR DB Module
import database.chroma_db as vectordb

# AI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from openai import OpenAI as SDKOpenAI

# DTO
from dto import openai_dto
from prompt import openai_prompt

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

# description: make fastapi app
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

@app.post("/chatgpt/langchain/case")
def get_langchain_case(data: openai_dto.PromptRequest):
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
    return chat_model.predict(prompt.format(question=question))


# case 1 : normal
@app.post("/chatgpt/langchain/normal")
def get_langchain_normal(data: openai_dto.PromptRequest): # case 1 : normal
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
@app.post("/chatgpt/langchain/make_schedule")
def get_langchain_schedule(data: openai_dto.PromptRequest):
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
@app.post("/chatgpt/langchain/rag")
def get_langchain_rag(data: openai_dto.PromptRequest):
    # description: use langchain
    chat_model = ChatOpenAI(temperature=0,  # 창의성 (0.0 ~ 2.0)
                            max_tokens=2048,  # 최대 토큰수
                            model_name='gpt-3.5-turbo-1106',  # 모델명
                            openai_api_key=OPENAI_API_KEY  # API 키
                            )
    question = data.prompt

    schedule = vectordb.search_db_query(question)  # vector db에서 검색

    # description: give NESS's ideal instruction as template
    case3_template = openai_prompt.Template.case3_template

    prompt = PromptTemplate.from_template(case3_template)
    return chat_model.predict(prompt.format(output_language="Korean", question=question, schedule=schedule))

if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", port=8000, app=app)
