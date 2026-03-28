from pydantic import BaseModel
from typing import Optional


class State(BaseModel):
    intent: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    next_action: Optional[str] = None
    reply: Optional[str] = None

class UserState(BaseModel):
    user_id: str
    state: State