import os
import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

def get_rds_connection():
    return pymysql.connect(
        host=os.getenv('RDS_HOST'),
        port=3306,
        user=os.getenv('RDS_USER'),
        password=os.getenv('RDS_PASSWORD'),
        database=os.getenv('RDS_DATABASE'),
        cursorclass=DictCursor
    )

def fetch_category_classification_data(member_id):
    connection = get_rds_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
            SELECT c.*
            FROM category c
            WHERE c.member_id = %s
            """
            cursor.execute(sql, (member_id,))
            result = cursor.fetchall()
            return result
    finally:
        connection.close()

def fetch_previous_conversations(member_id):
    connection = get_rds_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT c.text, c.chat_type
                FROM chat c
                WHERE c.member_id = %s
                ORDER BY c.created_date DESC
                LIMIT 5
                """
            cursor.execute(sql, (member_id,))
            result = cursor.fetchall()
            formatted_result = []
            for chat in result:
                # chat_type에 따라 'system' 또는 'human'으로 설정
                sender_type = 'ai' if chat['chat_type'] == 'AI' else 'human'
                # 메시지 포맷팅
                formatted_result.append((sender_type, chat['text']))
            return formatted_result[::-1]  # 최신 메시지가 마지막에 오도록 순서를 뒤집습니다.
            return result
    except Exception as e:
        print("Error fetching conversations:", e, file=sys.stderr)
        return []  # 오류 발생 시 빈 리스트 반환
    finally:
        connection.close()


