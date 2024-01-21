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
    my_template = openai_prompt.Template.case_template

    prompt = PromptTemplate.from_template(my_template)
    return chat_model.predict(prompt.format(question=question))


@app.post("/chatgpt/langchain/normal")
def get_langchain_normal():
    # description: use langchain
    chat_model = ChatOpenAI(temperature=0,  # 창의성 (0.0 ~ 2.0)
                            max_tokens=2048,  # 최대 토큰수
                            model_name='gpt-3.5-turbo-1106',  # 모델명
                            openai_api_key=OPENAI_API_KEY  # API 키
                            )
    # 기존 모델 문제 생김
    # chat_model = LangchainOpenAI(openai_api_key=OPENAI_API_KEY)

    # description: give NESS's ideal instruction as template
    my_template = """아래의 질문에 대해 한 줄로 간결하고 친절하게 답변하세요.
    질문: {question}"""

    prompt = PromptTemplate.from_template(my_template)
    return chat_model.predict(prompt.format(question="fastapi가 뭐야? 한 줄로 간결하고 친절하게 답변해줘."))


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
    my_template = """consider yourself as assistant who takes care of user's schedule,
    and answer the question refer to the user's schedule. Notice that you should answer in Korean.
    question: {question},
    schedule: {schedule}"""

    prompt = PromptTemplate.from_template(my_template)
    return chat_model.predict(prompt.format(question=question, schedule=schedule))


@app.post("/chatgpt/sdk/normal")
def get_sdk_normal():
    # description: only use OpenAI SDK
    client = SDKOpenAI(
        api_key=OPENAI_API_KEY
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "fastapi가 뭐야? 한 줄로 간결하고 친절하게 답변해줘.",
            }
        ],
        model="gpt-4",
    )
    return chat_completion.choices[0].message.content


@app.post("/chatgpt/sdk/rag")
def get_sdk_rag(data: openai_dto.PromptRequest):
    # description: only use OpenAI SDK
    client = SDKOpenAI(
        api_key=OPENAI_API_KEY
    )

    question = data.prompt  # 임시적으로 하드코딩

    schedule = vectordb.search_db_query(question)  # vector db에서 검색

    content = f"""consider yourself as assistant who takes care of user's schedule,
                and answer the question refer to the user's schedule. Notice that you should answer in Korean.
                question: {question},
                schedule: {schedule}"""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model="gpt-4",
    )
    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", port=8000, app=app)
