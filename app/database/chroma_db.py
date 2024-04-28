# VECTOR DB
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings

# FAST API
from fastapi import Depends

# ETC
import os
import datetime
from dotenv import load_dotenv
from app.dto.db_dto import AddScheduleDTO, RecommendationMainRequestDTO, ReportTagsRequestDTO

load_dotenv()
CHROMA_DB_IP_ADDRESS = os.getenv("CHROMA_DB_IP_ADDRESS")

# description: 원격 EC2 인스턴스에서 ChromaDB에 연결
# https://db.nessplanning.com
chroma_client = chromadb.HttpClient(host='https://db.nessplanning.com', port=8000)
# chroma_client = chromadb.HttpClient(host=CHROMA_DB_IP_ADDRESS, port=8000)

# description: embedding funtion 설정
# all-MiniLM-L6-v2 가 디폴트
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# description: collection "posts" 있으면 불러오고, 없으면 생성
# 각각의 데이터=document, 문서의 그룹핑=collection
schedules = chroma_client.get_or_create_collection(
    name="schedules",
    embedding_function=sentence_transformer_ef,
    metadata={"hnsw:space": "cosine"}  # 코사인 유사도로 검색(기타 옵션: l2(Squared L2), ip(Inner product)
)

# description: DB에 연결되었는지 확인하는 나노세컨드단위 heartbeat 생성 함수
def check_db_heartbeat():
    chroma_client.heartbeat()

# description: DB에서 검색하는 함수 - chat case 3에 사용
async def search_db_query(query):
    # 컬렉션 생성
    # 컬렉션에 쿼리 전송
    result = schedules.query(
        query_texts=query,
        n_results=5  # 결과에서 한 가지 문서만 반환하면 한강공원이, 두 가지 문서 반환하면 AI가 뜸->유사도가 이상하게 검사되는 것 같음
    )
    return result

# description: DB에 저장하는 함수
# 스프링 백엔드로부터 chroma DB에 저장할 데이터를 받아 DB에 추가한다.
async def add_db_data(schedule_data: AddScheduleDTO):
    schedule_date = schedule_data.schedule_datetime_start.split("T")[0]
    year = int(schedule_date.split("-")[0])
    month = int(schedule_date.split("-")[1])
    date = int(schedule_date.split("-")[2])
    schedules.add(
        documents=[schedule_data.data],
        ids=[str(schedule_data.schedule_id)],
        metadatas=[{"year": year, "month": month, "date": date, "datetime_start": schedule_data.schedule_datetime_start, "datetime_end": schedule_data.schedule_datetime_end, "member": schedule_data.member_id, "category": schedule_data.category, "location": schedule_data.location, "person": schedule_data.person}]
    )
    return True

# 메인페이지 한 줄 추천 기능에 사용하는 함수
# 유저의 id, 해당 날짜로 필터링
async def db_daily_schedule(user_data: RecommendationMainRequestDTO):
    member = user_data.member_id
    schedule_datetime_start = user_data.schedule_datetime_start
    schedule_datetime_end = user_data.schedule_datetime_end
    schedule_date = schedule_datetime_start.split("T")[0]
    year = int(schedule_date.split("-")[0])
    month = int(schedule_date.split("-")[1])
    date = int(schedule_date.split("-")[2])
    persona = user_data.user_persona or "hard working"
    results = schedules.query(
        query_texts=[persona],
        n_results=5,
        where={"$and":
               [
                   {"member": {"$eq": int(member)}},
                   {"year": {"$eq": year}},
                   {"month": {"$eq": month}},
                   {"date": {"$eq": date}}
               ]
        }
        # where_document={"$contains":"search_string"}  # optional filter
    )
    return results['documents']

# 태그 생성용 스케쥴 반환 - 카테고리에 따라
async def db_monthly_tag_schedule(user_data: ReportTagsRequestDTO):
    member = user_data.member_id
    schedule_datetime_start = user_data.schedule_datetime_start
    schedule_datetime_end = user_data.schedule_datetime_end
    schedule_date = schedule_datetime_start.split("T")[0]
    year = int(schedule_date.split("-")[0])
    month = int(schedule_date.split("-")[1])
    date = int(schedule_date.split("-")[2])
    persona = user_data.user_persona or "hard working"
    results = schedules.query(
        query_texts=[persona],
        n_results=15,
        where={"$and":
               [
                   {"member": {"$eq": int(member)}},
                   {"year": {"$eq": year}},
                   {"month": {"$eq": month - 1}}
                   # {"$or":
                   #  [{"$and":
                   #        [{"month": {"$eq": month-1}}, {"date": {"$gte": 10}}]},
                   #   {"$and":
                   #        [{"month": {"$eq": month}}, {"date": {"$lt": 10}}]}
                   #  ]}
               ]
        }
        # where_document={"$contains":"search_string"}  # optional filter
    )
    return results['documents']

def get_chroma_client():
    return chroma_client