# VECTOR DB
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings

# ETC
import os
import datetime
from dotenv import load_dotenv
from app.dto.db_dto import AddScheduleDTO

load_dotenv()
CHROMA_DB_IP_ADDRESS = os.getenv("CHROMA_DB_IP_ADDRESS")
# # 로컬에 ChromaDB가 저장된 경우
# DIR = os.path.dirname(os.path.abspath(__file__))
# DB_PATH = os.path.join(DIR, 'data')
# # 로컬 디스크에서 ChromaDB 실행: allow_reset으로 데이터베이스 초기화, anonymized_telemetry를 False로 설정하여 텔레메트리 수집 비활성화
# chroma_client = chromadb.PersistentClient(path=DB_PATH,
#                                           settings=Settings(allow_reset=True, anonymized_telemetry=False))

# description: 원격 EC2 인스턴스에서 ChromaDB에 연결
chroma_client = chromadb.HttpClient(host=CHROMA_DB_IP_ADDRESS, port=8000)

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

# description: DB에서 검색하는 함수
async def search_db_query(query):
    # 컬렉션 생성
    # 컬렉션에 쿼리 전송
    result = schedules.query(
        query_texts=query,
        n_results=2  # 결과에서 한 가지 문서만 반환하면 한강공원이, 두 가지 문서 반환하면 AI가 뜸->유사도가 이상하게 검사되는 것 같음
    )
    return result

# description: DB에 저장하는 함수
# 스프링 백엔드로부터 chroma DB에 저장할 데이터를 받아 DB에 추가한다.
async def add_db_data(schedule_data: AddScheduleDTO):
    schedules.add(
        documents=[schedule_data.data],
        ids=[str(schedule_data.schedule_id)],
        metadatas=[{"datetime": schedule_data.schedule_datetime, "member": schedule_data.member_id, "category": schedule_data.category}]
    )
    return True