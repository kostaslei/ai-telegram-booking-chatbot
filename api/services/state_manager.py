from data.store import user_states


def get_state(user_id: str):
    return user_states.get(user_id, {})


def update_state(user_id: str, new_state: dict):
    current = user_states.get(user_id, {})

    updated = {**current, **new_state}

    user_states[user_id] = updated
    return updated


def clear_state(user_id: str):
    user_states.pop(user_id, None)