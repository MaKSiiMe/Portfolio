from typing import Any
from lemon_tcg.event.response_type import EventResponseType

class EventResponse():
    def __init__(self, type: EventResponseType, data: Any) -> None:
        self.type = type
        self.data = data

    @staticmethod
    def success(data: Any = None) -> 'EventResponse':
        return EventResponse(type=EventResponseType.SUCCESS, data=data)
    
    @staticmethod
    def multi(responses: list['EventResponse'] = []) -> 'EventResponse':
        return EventResponse(type=EventResponseType.MULTI, data=responses)