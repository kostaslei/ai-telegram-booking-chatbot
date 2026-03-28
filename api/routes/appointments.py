from fastapi import APIRouter, Query
from schemas.booking import BookingRequest, CancelRequest
from services.scheduler import (
    get_available_dates,
    get_slots,
    book_slot,
    cancel_booking
)

router = APIRouter()

# GET available dates
@router.get("/available-dates")
def available_dates():
    data = get_available_dates()
    return {"dates": data}

# GET availability
@router.get("/availability")
def availability(date: str = Query(...)):
    slots = get_slots(date)
    return {"slots": slots}


# POST book
@router.post("/book")
def book(data: BookingRequest):
    result = book_slot(data.user_id, data.date, data.slot)
    return result


# POST cancel
@router.post("/cancel")
def cancel(data: CancelRequest):
    result = cancel_booking(data.user_id)
    return result


# GET user's booking
@router.get("/my-booking/{user_id}")
def my_booking(user_id: str):
    from data.store import bookings

    booking = next((b for b in bookings if b["user_id"] == user_id), None)

    return {"booking": booking}

