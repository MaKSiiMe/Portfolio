from typing import Callable
from lemon_tcg.event.response import EventResponse
from lemon_tcg.exceptions import EventNotRegisteredError, EventExecutionError

class EventBus():
    _instance = None

    def __init__(self) -> None:
        if EventBus._instance is not None:
            raise RuntimeError("Tried to initialize multiple instances of EventBus.")
        self.listeners: dict[str, list[Callable]] = {}
        
    @staticmethod
    def get_instance() -> 'EventBus':
        if EventBus._instance is None:
            EventBus._instance = EventBus()
        return EventBus._instance
    
    def register_event_listener(self, signal: str, listener: Callable) -> None:
        if signal not in self.listeners:
            self.listeners[signal] = []
        if listener not in self.listeners[signal]:
            self.listeners[signal].append(listener)

    async def dispatch_event(self, signal: str, **kwargs) -> EventResponse:
        if signal not in self.listeners:
            raise EventNotRegisteredError(signal=signal)
        responses = []
        for listener in self.listeners[signal]:
            try:
                response = await listener(**kwargs)
                assert isinstance(response, EventResponse)
            except Exception as error:
                raise EventExecutionError(error=error, signal=signal)
            responses.append(response)
        
        if len(responses) == 1:
            return responses[0]
        return EventResponse.multi(responses=responses)