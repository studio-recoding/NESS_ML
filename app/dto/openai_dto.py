from pydantic import BaseModel
from typing import List

class PromptRequest(BaseModel):
    prompt: str
    persona: str

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

<<<<<<< Updated upstream
class ActivityDescription(BaseModel):
    activity: str
    imageTag: str

class RecommendationResponse(BaseModel):
    ness: str
    activityList: List[ActivityDescription]
=======
class ActivityInfo(BaseModel):
    activity: str
    imageTag: str
class RecommendationResponse(BaseModel):
    ness: str
    activityList: List[ActivityInfo]
>>>>>>> Stashed changes
