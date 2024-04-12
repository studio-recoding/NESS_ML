from pydantic import BaseModel
from typing import List

class PromptRequest(BaseModel):
    prompt: str

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