from enum import Enum

class EventType(Enum):
    DRAW_CARD = "draw_card"
    GAME_STATE_TICK = "game_state_tick"

    def with_id(self, id: str) -> str:
        return f"{self.value}_{id}"
    
    def with_id_index(self, id: str, index: int) -> str:
        return f"{self.value}_{index}_{id}"