from datetime import datetime

def current_timestamp() -> float:
    return datetime.now().timestamp()