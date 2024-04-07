from pydantic import BaseModel


class PromptRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    ness: str

class ChatCaseResponse(BaseModel):
    ness: str
    case: int