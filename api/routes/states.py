from fastapi import APIRouter
from schemas.state import UserState
from services.state_manager import get_state, update_state, clear_state

router = APIRouter()


@router.get("/state/{user_id}")
def read_state(user_id: str):
    return get_state(user_id)


@router.post("/state")
def write_state(payload: UserState):
    updated = update_state(payload.user_id, payload.state.dict())
    return {"success": True, "state": updated}


@router.delete("/state/{user_id}")
def delete_state(user_id: str):
    clear_state(user_id)
    return {"success": True}