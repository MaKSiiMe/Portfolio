import asyncio
from typing import Any, Optional
from lemon_tcg.event.bus import EventBus
from lemon_tcg.event.response import EventResponse
from lemon_tcg.event.type import EventType

BUS = EventBus.get_instance()

def get_signal_name(event_type: EventType, game_state_id: str, index: Optional[int] = None) -> str:
    if not isinstance(index, int):
        return event_type.with_id(id=game_state_id)
    else:
        return event_type.with_id_index(id=game_state_id, index=index)

async def dispatch_event(event_type: EventType, game_state_id: str, index: Optional[int] = None, **kwargs) -> EventResponse:
    """Will dispatch an event for the given event type.

    Args:
        event_type (EventType): The type of event.
        game_state_id (str): The id of the game state to modify.
        index (Optional[int], optional): An optional index for further granularity. Defaults to None.
    """
    signal_name = get_signal_name(event_type=event_type, game_state_id=game_state_id, index=index)
    response = await BUS.dispatch_event(signal=signal_name, **kwargs)
    return response

def register_event_listener(event_type: EventType, game_state_id: str, listener, index: Optional[int] = None) -> None:
    """Will register an event listener for the given event type.

    Args:
        event_type (EventType): The type of event.
        game_state_id (str): The id of the game state.
        listener (_type_): The event listener.
        index (Optional[int], optional): An optional index for further granularity. Defaults to None.
    """
    signal_name = get_signal_name(event_type=event_type, game_state_id=game_state_id, index=index)
    BUS.register_event_listener(signal=signal_name, listener=listener)