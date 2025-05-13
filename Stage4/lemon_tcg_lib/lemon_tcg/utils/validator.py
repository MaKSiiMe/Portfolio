def validate_user_index(user_index: int) -> None:
    if user_index < 0 or user_index > 1:
        raise RuntimeError(f"User index out of range.")