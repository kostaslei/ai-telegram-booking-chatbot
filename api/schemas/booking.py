from pydantic import BaseModel

class BookingRequest(BaseModel):
    user_id: str
    date: str
    slot: str

class CancelRequest(BaseModel):
    user_id: str

class BookingResponse(BaseModel):
    success: bool
    message: str | None = None
    booking: dict | None = None