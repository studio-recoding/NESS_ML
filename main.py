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


# case 1 : normal
@app.post("/chatgpt/langchain/normal")
def get_langchain_normal(): # case 1 : normal
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
    case2_template = """
    You are a friendly assistant who helps users manage their schedules. The user's input contains information about a new event they want to add to their schedule. You have two tasks to perform:

    1. Respond kindly to the user's input. YOU MUST USE {output_language} TO RESPOND TO THE USER INPUT.
    2. Organize the event the user wants to add into a json format for saving in a database. The returned json will have keys for info, location, person, and date.
    - info: Summarizes what the user wants to do. This value must always be present.
    - location: If the user's event information includes a place, save that place as the value.
    - person: If the user's event mentions a person they want to include, save that person as the value.
    - date: If the user's event information includes a specific date and time, save that date and time in datetime format.
    Separate the outputs for tasks 1 and 2 with a special token <separate>.
    
    Example for one-shot learning:

    User input: "I have a meeting with Dr. Smith at her office on March 3rd at 10am."
    
    Response to user:
    "I've added your meeting with Dr. Smith at her office on March 3rd at 10am to your schedule. Is there anything else you'd like to add or modify?"
    <separate>
    {{
        "info": "meeting with Dr. Smith",
        "location": "Dr. Smith's office",
        "person": "Dr. Smith",
        "date": "2023-03-03T10:00:00"
    }}
    
    User input: {question}
    """

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
    my_template = """consider yourself as assistant who takes care of user's schedule,
    and answer the question refer to the user's schedule. Notice that you should answer in Korean.
    question: {question},
    schedule: {schedule}"""

    prompt = PromptTemplate.from_template(my_template)
    return chat_model.predict(prompt.format(question=question, schedule=schedule))


# @app.post("/chatgpt/sdk/normal")
# def get_sdk_normal():
#     # description: only use OpenAI SDK
#     client = SDKOpenAI(
#         api_key=OPENAI_API_KEY
#     )
#
#     chat_completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": "fastapi가 뭐야? 한 줄로 간결하고 친절하게 답변해줘.",
#             }
#         ],
#         model="gpt-4",
#     )
#     return chat_completion.choices[0].message.content
#
#
# @app.post("/chatgpt/sdk/rag")
# def get_sdk_rag(data: openai_dto.PromptRequest):
#     # description: only use OpenAI SDK
#     client = SDKOpenAI(
#         api_key=OPENAI_API_KEY
#     )
#
#     question = data.prompt  # 임시적으로 하드코딩
#
#     schedule = vectordb.search_db_query(question)  # vector db에서 검색
#
#     content = f"""consider yourself as assistant who takes care of user's schedule,
#                 and answer the question refer to the user's schedule. Notice that you should answer in Korean.
#                 question: {question},
#                 schedule: {schedule}"""
#
#     chat_completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": content,
#             }
#         ],
#         model="gpt-4",
#     )
#     return chat_completion.choices[0].message.content


if __name__ == "__main__":
    uvicorn.run(host="0.0.0.0", port=8000, app=app)
