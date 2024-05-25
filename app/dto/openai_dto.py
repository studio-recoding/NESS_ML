from pydantic import BaseModel
from typing import List

class PromptRequest(BaseModel):
    member_id: int
    prompt: str
    persona: str
    chatType: str

class ChatResponse(BaseModel):
    ness: str

class ChatCaseResponse(BaseModel):
    ness: str
    case: int

class TagDescription(BaseModel):
    tag: str
    desc: str

class TagsResponse(BaseModel):
    tagList: List[TagDescription]

class EmailResponse(BaseModel):
    text: str
    image: str

class ActivityDescription(BaseModel):
    activity: str
    imageTag: str

class RecommendationResponse(BaseModel):
    ness: str
    activityList: List[ActivityDescription]

