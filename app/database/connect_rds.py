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
