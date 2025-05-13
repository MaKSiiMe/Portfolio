from lemon_tcg.event.type import EventType
from lemon_tcg.event.helper import dispatch_event

async def game_state_tick(game_state_id: str) -> None:
    """Will tick up the game states event_tick.

    Args:
        game_state_id (str): The id of the game state to tick up.
    """
    await dispatch_event(event_type=EventType.GAME_STATE_TICK, game_state_id=game_state_id)