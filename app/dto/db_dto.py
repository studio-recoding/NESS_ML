from pydantic import BaseModel
from datetime import datetime  # datetime 클래스를 직접 임포트합니다.

class AddScheduleDTO(BaseModel):
    data: str
    schedule_datetime_start: str  # datetime.datetime 타입을 명시적으로 사용합니다.
    schedule_datetime_end: str
    schedule_id: int
    member_id: int
    category: str
    category_id: int
    location: str
    person: str

class DeleteScheduleDTO(BaseModel):
    schedule_id: int
    member_id: int

class UpdateScheduleDTO(BaseModel):
    data: str
    schedule_datetime_start: str
    schedule_datetime_end: str
    schedule_id: int
    member_id: int
    category: str
    category_id: int
    location: str
    person: str

class RecommendationMainRequestDTO(BaseModel):
    member_id: int
    user_persona: str
    schedule_datetime_start: str
    schedule_datetime_end: str

class ReportMemoryEmojiRequestDTO(BaseModel):
    member_id: int
    user_persona: str
    schedule_datetime_start: str
    schedule_datetime_end: str

class ReportTagsRequestDTO(BaseModel):
    member_id: int
    user_persona: str
    schedule_datetime_start: str
    schedule_datetime_end: str

class EmailRequestDTO(BaseModel):
    member_id: int
    user_persona: str
    schedule_datetime_start: str
    schedule_datetime_end: str

