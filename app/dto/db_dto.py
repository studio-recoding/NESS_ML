from pydantic import BaseModel
from datetime import datetime  # datetime 클래스를 직접 임포트합니다.

class AddScheduleDTO(BaseModel):
    data: str
    schedule_datetime_start: str  # datetime.datetime 타입을 명시적으로 사용합니다.
    schedule_datetime_end: str
    schedule_id: int
    member_id: int
    category: str
    location: str
    person: str

