import configparser
import os
import json

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, status, HTTPException
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from app.dto.db_dto import RecommendationMainRequestDTO
from app.dto.openai_dto import RecommendationResponse, ActivityDescription
from app.dto.openai_dto import CategoryInfo, RecommendationSchedule, ListRecommendationPair, ListRecommendationRequest, ListRecommendationResponse
from app.prompt import openai_prompt, persona_prompt
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

# 유저의 하루 스케줄을 기반으로 한 줄 추천 & 추천 활동을 생성한다.
@router.post("/main", status_code=status.HTTP_200_OK)
async def get_recommendation(user_data: RecommendationMainRequestDTO) -> RecommendationResponse:
    try:
        # 모델
        config_recommendation = config['NESS_RECOMMENDATION']

        chat_model = ChatOpenAI(temperature=config_recommendation['TEMPERATURE'],  # 창의성 (0.0 ~ 2.0)
                                max_tokens=config_recommendation['MAX_TOKENS'],  # 최대 토큰수
                                model_name=config_recommendation['MODEL_NAME'],  # 모델명
                                openai_api_key=OPENAI_API_KEY  # API 키
                                )

        # vectordb에서 유저의 정보를 가져온다.
        day_schedule = await vectordb.db_daily_schedule(user_data)

        print(day_schedule)

        # 템플릿
        recommendation_template = openai_prompt.Template.recommendation_template
        persona = user_data.user_persona
        user_persona_prompt = persona_prompt.Template.from_persona(persona)

        prompt = PromptTemplate.from_template(recommendation_template)
        ness = chat_model.predict(prompt.format(persona=user_persona_prompt,
                                                output_language="Korean",
                                                schedule=day_schedule
                                                ))
        print(ness)

        # 한 줄 추천 기반 활동 추천하기
        month_schedule = await vectordb.activity_recommendation_schedule(user_data, ness)
        print(month_schedule)

        activity_template = openai_prompt.Template.activity_template
        activity_prompt = PromptTemplate.from_template(activity_template)
        activity_response = chat_model.predict(activity_prompt.format(persona=user_persona_prompt,
                                                                      output_language="Korean",
                                                                      schedule=month_schedule
                                                                      ))
        print(activity_response)

        try:
            activities = json.loads(activity_response)
        except json.JSONDecodeError:
            print("Error parsing the JSON response")
            activities = []

        # Generate ActivityDescription objects
        activity_list = [ActivityDescription(activity=act, imageTag=act.replace(" ", "_").lower() + "_img") for act in
                         activities]

        # Create the RecommendationResponse object
        response = RecommendationResponse(ness=ness, activityList=activity_list)

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/list", status_code=status.HTTP_200_OK)
async def get_recommendation_list(user_data: ListRecommendationRequest) -> ListRecommendationResponse:
    try:
        # 모델 설정
        config_recommendation = config['NESS_RECOMMENDATION']

        chat_model = ChatOpenAI(
            temperature=config_recommendation['TEMPERATURE'],  # 창의성 (0.0 ~ 2.0)
            max_tokens=config_recommendation['MAX_TOKENS'],  # 최대 토큰수
            model_name=config_recommendation['MODEL_NAME'],  # 모델명
            openai_api_key=OPENAI_API_KEY  # API 키
        )

        # 프롬프트 템플릿 설정
        recommendation_list_prompt = PromptTemplate.from_template(openai_prompt.Template.recommendation_list_template)
        # 일정 리스트를 포맷팅
        schedule_list = "\n".join([
            f"Start Time: {schedule.startTime if schedule.startTime else 'not specified'}\n"
            f"Category: {schedule.category.categoryName if schedule.category.categoryName else 'not specified'} (ID: {schedule.category.categoryId if schedule.category.categoryId else 'not specified'}, Color: {schedule.category.categoryColor if schedule.category.categoryColor else 'not specified'})\n"
            f"Person: {schedule.person if schedule.person else 'not specified'}\n"
            f"Location: {schedule.location if schedule.location else 'not specified'}\n"
            f"Info: {schedule.info if schedule.info else 'not specified'}\n"
            for schedule in user_data.todoList
        ])

        # 하나의 프롬프트로 일정 리스트를 전달
        recommendation_response = chat_model.predict(recommendation_list_prompt.format(
            persona=user_data.persona,
            output_language="Korean",
            schedule_list=schedule_list
        ))

        # 응답을 리스트 형식으로 파싱
        comments = eval(recommendation_response.strip())

        # 응답을 포맷팅하여 리스트로 반환
        recommendations = [
            ListRecommendationPair(
                todo=schedule,
                nessComment=comment
            )
            for schedule, comment in zip(user_data.todoList, comments)
        ]

        return ListRecommendationResponse(recommendationList=recommendations)

        return ListRecommendationResponse(recommendationList=recommendations)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
