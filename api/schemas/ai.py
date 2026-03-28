from pydantic import BaseModel
from typing import Optional


class AIRequest(BaseModel):
    message: str
    state: dict


class AIResponse(BaseModel):
    intent: str
    date: Optional[str] = None
    time: Optional[str] = None
    next_action: str
    reply: str