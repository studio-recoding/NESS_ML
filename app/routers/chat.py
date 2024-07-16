# app/routers/chat.py
import configparser
import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, status
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from datetime import datetime

from app.database.connect_rds import fetch_category_classification_data, fetch_previous_conversations
from app.dto.openai_dto import PromptRequest, ChatResponse, ChatCaseResponse
from app.prompt import openai_prompt, persona_prompt

import app.database.chroma_db as vectordb
import pytz

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

@router.post("/case", status_code=status.HTTP_200_OK, response_model=ChatCaseResponse)
async def get_langchain_case(data: PromptRequest) -> ChatCaseResponse:
    # description: use langchain

    config_chat = config['NESS_CASE']

    chat_model = ChatOpenAI(temperature=config_chat['TEMPERATURE'],  # 창의성 (0.0 ~ 2.0)
                            max_tokens=config_chat['MAX_TOKENS'],  # 최대 토큰수
                            model_name=config_chat['MODEL_NAME'],  # 모델명
                            openai_api_key=OPENAI_API_KEY  # API 키
                            )
    question = data.prompt # 유저로부터 받은 채팅의 내용
    chat_type = data.chatType # 위스퍼 사용 여부 [STT, USER]

    # description: give NESS's instruction as for case analysis
    my_template = openai_prompt.Template.case_classify_template

    # chat type에 따라 적합한 프롬프트를 삽입
    if chat_type == "STT":
        chat_type_prompt = openai_prompt.Template.chat_type_stt_template
    elif chat_type == "USER":
        chat_type_prompt = openai_prompt.Template.chat_type_user_template
    else:
        raise HTTPException(status_code=500, detail="WRONG CHAT TYPE")

    prompt = PromptTemplate.from_template(my_template)
    case = chat_model.predict(prompt.format(question=question, chat_type=chat_type_prompt))

    # 각 케이스에도 chat type에 따라 적합한 프롬프트 삽입 필요
    print(case)
    case = int(case)
    if case == 1:
        response = await get_langchain_normal(data, chat_type_prompt)
        metadata = "null"

    elif case == 2:
        response_with_metadata = await get_langchain_schedule(data, chat_type_prompt)
        response = response_with_metadata.split("<separate>")[0]
        metadata = response_with_metadata.split("<separate>")[1]

    elif case == 3:
        response = await get_langchain_rag(data, chat_type_prompt)
        metadata = "null"

    elif case == 4:
        response_with_metadata = await delete_schedule(data, chat_type_prompt)
        response = response_with_metadata.split("<separate>")[0]
        metadata = response_with_metadata.split("<separate>")[1]

    else:
        response = "좀 더 명확한 요구가 필요해요. 다시 한 번 얘기해주실 수 있나요?"
        case = "Exception"
        metadata = "null"

    return ChatCaseResponse(ness=response, case=case, metadata=metadata)


# case 1 : normal
#@router.post("/case/normal") # 테스트용 엔드포인트
async def get_langchain_normal(data: PromptRequest, chat_type_prompt): # case 1 : normal
    print("running case 1")
    # description: use langchain
    config_normal = config['NESS_NORMAL']

    chat_model = ChatOpenAI(temperature=config_normal['TEMPERATURE'],  # 창의성 (0.0 ~ 2.0)
                            max_tokens=config_normal['MAX_TOKENS'],  # 최대 토큰수
                            model_name=config_normal['MODEL_NAME'],  # 모델명
                            openai_api_key=OPENAI_API_KEY  # API 키
                            )
    # 유저 입력
    question = data.prompt
    # 페르소나 프롬프트
    persona = data.persona
    user_persona_prompt = persona_prompt.Template.from_persona(persona)

    # 현재 시각 설정
    seoul_timezone = pytz.timezone('Asia/Seoul')
    current_time = datetime.now(seoul_timezone)
    print(f'current time: {current_time}')

    # 이전 대화내역 불러오기
    previous_conversations = fetch_previous_conversations(data.member_id)
    print(previous_conversations)

    # case 1 프롬프트
    case1_template = openai_prompt.Template.case1_template
    #prompt = PromptTemplate.from_template(my_template)
    # system, human, ai
    chat_prompt = ChatPromptTemplate.from_messages(
        previous_conversations + [
            ("system", case1_template),
            ("human", "{question}")
        ]
    )

    # 프롬프트와 모델을 chaining
    chain = chat_prompt | chat_model

    #response = chat_model.predict(prompt.format(persona=user_persona_prompt, output_language="Korean", question=question, current_time=current_time, chat_type=chat_type_prompt))
    response = chain.invoke({
        "persona": user_persona_prompt,
        "output_language": "Korean",
        "current_time": current_time,
        "chat_type": chat_type_prompt,
        "question": question
    })
    print(response.content)
    return response.content

# case 2 : 일정 생성
#@router.post("/case/make_schedule") # 테스트용 엔드포인트
async def get_langchain_schedule(data: PromptRequest, chat_type_prompt):
    try:
        print("running case 2")
        config_normal = config['NESS_NORMAL']

        chat_model = ChatOpenAI(temperature=config_normal['TEMPERATURE'],  # 창의성 (0.0 ~ 2.0)
                                max_tokens=config_normal['MAX_TOKENS'],  # 최대 토큰수
                                model_name=config_normal['MODEL_NAME'],  # 모델명
                                openai_api_key=OPENAI_API_KEY  # API 키
                                )

        member_id = data.member_id

        # 카테고리 가져오기
        categories = fetch_category_classification_data(member_id)
        # 카테고리 데이터를 딕셔너리 형태로 변환
        categories_dict = [
            {"name": category['name'], "id": category['category_id'], "color": category['color']}
            for category in categories
        ]

        # 시간 가져오기
        seoul_timezone = pytz.timezone('Asia/Seoul')
        current_time = datetime.now(seoul_timezone)
        print(f'current time: {current_time}')

        # 이전 대화 내역 가져오기
        previous_conversations = fetch_previous_conversations(member_id)
        print(previous_conversations)

        question = data.prompt
        persona = data.persona
        user_persona_prompt = persona_prompt.Template.from_persona(persona)

        # case 2 프롬프트
        case2_template = openai_prompt.Template.case2_template
        # prompt = PromptTemplate.from_template(case2_template)
        # system, human, ai
        chat_prompt = ChatPromptTemplate.from_messages(
            previous_conversations + [
                ("system", case2_template),
                ("human", "User input: {question}")
            ]
        )


        # # OpenAI 프롬프트에 데이터 통합
        # response = chat_model.predict(
        #     prompt.format(
        #         persona=user_persona_prompt,
        #         output_language="Korean",
        #         question=question,
        #         current_time=current_time,
        #         chat_type=chat_type_prompt,
        #         categories=categories_dict  # 카테고리 데이터를 프롬프트에 포함
        #     )
        # )

        # 프롬프트와 모델을 chaining
        chain = chat_prompt | chat_model

        # response = chat_model.predict(prompt.format(persona=user_persona_prompt, output_language="Korean", question=question, current_time=current_time, chat_type=chat_type_prompt))
        response = chain.invoke({
            "persona": user_persona_prompt,
            "output_language": "Korean",
            "current_time": current_time,
            "chat_type": chat_type_prompt,
            "categories": categories_dict,
            "question": question
        })

        print(response.content)
        return response.content

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

# case 3 : rag
#@router.post("/case/rag") # 테스트용 엔드포인트
async def get_langchain_rag(data: PromptRequest, chat_type_prompt):
    print("running case 3")
    # description: use langchain
    config_normal = config['NESS_NORMAL']

    chat_model = ChatOpenAI(temperature=config_normal['TEMPERATURE'],  # 창의성 (0.0 ~ 2.0)
                            max_tokens=config_normal['MAX_TOKENS'],  # 최대 토큰수
                            model_name=config_normal['MODEL_NAME'],  # 모델명
                            openai_api_key=OPENAI_API_KEY  # API 키
                            )

    member_id = data.member_id
    question = data.prompt
    persona = data.persona
    user_persona_prompt = persona_prompt.Template.from_persona(persona)

    # 시간 가져오기
    seoul_timezone = pytz.timezone('Asia/Seoul')
    current_time = datetime.now(seoul_timezone)
    print(f'current time: {current_time}')

    # 관련 스케줄 가져오기
    schedule = await vectordb.search_db_query(member_id, question)  # vector db에서 검색

    # 이전 대화 내역 불러오기
    previous_conversations = fetch_previous_conversations(member_id)
    print(previous_conversations)

    # description: give NESS's ideal instruction as template
    case3_template = openai_prompt.Template.case3_template
    case3_user = """
    User input: {question},
    RAG Retrieval: {schedule}
    Response:
    """
    #prompt = PromptTemplate.from_template(case3_template)
    # system, human, ai
    chat_prompt = ChatPromptTemplate.from_messages(
        previous_conversations + [
            ("system", case3_template),
            ("human", case3_user)
        ]
    )

    #response = chat_model.predict(prompt.format(persona=user_persona_prompt, output_language="Korean", question=question, schedule=schedule, current_time=current_time, chat_type=chat_type_prompt))
    # 프롬프트와 모델을 chaining
    chain = chat_prompt | chat_model

    response = chain.invoke({
        "persona": user_persona_prompt,
        "output_language": "Korean",
        "current_time": current_time,
        "chat_type": chat_type_prompt,
        "schedule": schedule,
        "question": question
    })
    print(response.content)
    return response.content

# case 4 : delete schedule
async def delete_schedule(data: PromptRequest, chat_type_prompt):
    print("running case 4: delete schedule")

    config_normal = config['NESS_NORMAL']

    chat_model = ChatOpenAI(temperature=config_normal['TEMPERATURE'],  # 창의성 (0.0 ~ 2.0)
                            max_tokens=config_normal['MAX_TOKENS'],  # 최대 토큰수
                            model_name=config_normal['MODEL_NAME'],  # 모델명
                            openai_api_key=OPENAI_API_KEY  # API 키
                            )
    member_id = data.member_id
    question = data.prompt
    persona = data.persona
    user_persona_prompt = persona_prompt.Template.from_persona(persona)

    # 시간 정보 가져오기
    seoul_timezone = pytz.timezone('Asia/Seoul')
    current_time = datetime.now(seoul_timezone)
    print(f'current time: {current_time}')

    # vectordb.search_db_query를 호출
    schedule = await vectordb.search_db_query_delete(member_id, question)

    # 이전 대화 내역 불러오기
    previous_conversations = fetch_previous_conversations(member_id)
    print(previous_conversations)

    # description: give NESS's ideal instruction as template
    case4_template = openai_prompt.Template.case4_template
    case4_user = """     
    User input: {question}
    
    Schedules: {schedule}
    
    Response to user:
    """
    # system, human, ai
    chat_prompt = ChatPromptTemplate.from_messages(
        previous_conversations + [
            ("system", case4_template),
            ("human", case4_user)
        ]
    )

    # prompt = PromptTemplate.from_template(case4_template)
    chain = chat_prompt | chat_model

    response = chain.invoke({
        "persona": user_persona_prompt,
        "output_language": "Korean",
        "current_time": current_time,
        "chat_type": chat_type_prompt,
        "schedule": schedule,
        "question": question
    })
    print(response.content)
    return response.content
    #response = chat_model.predict(prompt.format(persona=user_persona_prompt, output_language="Korean", question=question, schedule=schedule, current_time=current_time, chat_type=chat_type_prompt))
    # print(response)
    # return response
