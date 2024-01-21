# VECTOR DB
import chromadb
from chromadb.config import Settings

# ETC
import os
import time

# chroma_client = chromadb.Client()

# 로컬에 chromadb가 저장된 경우
DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DIR, 'data')

# 로컬 디스크에서 chromadb 실행: allow_reset으로 데이터베이스 초기화
chroma_client = chromadb.PersistentClient(path=DB_PATH,
                                          settings=Settings(allow_reset=True, anonymized_telemetry=False))

# 기타 옵션: 원격에 chromadb가 있는 경우(실제 서비스 시 권장)
# chroma run --path C:\Users\414ca\Desktop\NESS_AI\database\data
# chroma_client = chromadb.HttpClient(host='localhost', port=8000)
# 기타 옵션: 메모리에 chromadb가 있는 경우
# chroma_client = chromadb.EphemeralClient()

# description: collection "posts" 있으면 불러오고, 없으면 생성
# 각각의 데이터=document, 문서의 그룹핑=collection
schedules = chroma_client.get_or_create_collection(
    name="schedules",
    metadata={"hnsw:space": "cosine"}  # 코사인 유사도로 검색(기타 옵션: l2(Squared L2), ip(Inner product)
)

# 임시적으로 하드코딩한 기존 문서들
post1 = '친구들과 함께 한강공원 놀러가기'
post2 = '프로젝트 미팅하기'
post3 = '학교에서 AI 공부하기'
post4 = '코딩 공부할 책 구입하기'
now_time = time.localtime()
schedules.add(
    documents=[post1, post2, post3, post4],
    ids=["1", "2", "3", "4"],
    metadatas=[{"time": str(now_time)}, {"time": str(now_time)}, {"time": str(now_time)}, {"time": str(now_time)}]
)


# description: DB에 연결되었는지 확인하는 나노세컨드단위 heartbeat 생성 함수
def check_db_heartbeat():
    chroma_client.heartbeat()


# description: DB에서 검색하는 함수
def search_db_query(query):
    # 컬렉션 생성
    # 컬렉션에 쿼리 전송
    result = schedules.query(
        query_texts=query,
        n_results=2  # 결과에서 한 가지 문서만 반환하면 한강공원이, 두 가지 문서 반환하면 AI가 뜸->유사도가 이상하게 검사되는 것 같음
    )
    return result


# description: DB에 저장하는 함수
def add_db_data(data):
    now_time = time.localtime()
    schedules.add(
        documents=[data],  # 문서만 전달하면 자동으로 토큰화 및 임베딩(기본적으로 all-MiniLM-L6-v2 모델 사용해 임베딩, 컴퓨터에서 로컬로 실행)
        ids=["1"],  # 일단 임시적으로 id를 하드코딩-실제로는 모든 docs마다 달라야 함
        metadatas=[{"time": str(now_time)}]  # 메타데이터 전달도 가능
    )
    return True
