from datetime import datetime,timedelta
from data.store import bookings, availability


def get_slots(date: str):
    return availability.get(date, [])

def get_available_dates():
    return [date for date, slots in availability.items() if slots]


def book_slot(user_id: str, date: str, time: str):
    slots = availability.get(date, [])

    if time not in slots:
        return {"success": False, "message": "Slot not available"}

    # remove slot (simulate booking)
    availability[date].remove(time)

    booking = {
        "user_id": user_id,
        "date": date,
        "time": time
    }

    bookings.append(booking)

    return {"success": True, "booking": booking}


def cancel_booking(user_id: str):
    for i, b in enumerate(bookings):
        if b["user_id"] == user_id:
            removed = bookings.pop(i)
            return {"success": True, "booking": removed}

    return {"success": False, "message": "No booking found"}