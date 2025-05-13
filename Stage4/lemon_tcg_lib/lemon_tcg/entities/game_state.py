from typing import Any
import uuid
from lemon_tcg.event.type import EventType
from lemon_tcg.entities.base_save_state_entity_group import BaseSaveStateEntityGroup
from lemon_tcg.entities.board import Board
from lemon_tcg.entities.player import Player
from lemon_tcg.event.helper import register_event_listener
from lemon_tcg.event.response import EventResponse
from lemon_tcg.utils.file_operations import construct_path
from lemon_tcg.utils.time_operations import current_timestamp

class GameState(BaseSaveStateEntityGroup):
    FILE_PATH = construct_path("lemon_tcg/data/save/games/{id}.json")
    board: Board = Board()
    players: list[Player] = []
    event_tick: int = 0
    start_stamp: float = current_timestamp()
    last_update_stamp: float = 0

    def model_post_init(self, __context: Any) -> None:
        self.register_events()
        self.board.register_events(dispatch_id=self.id)
        for player in self.players:
            player.register_events(dispatch_id=self.id)

    @staticmethod
    def create_new(players: list[Player]) -> 'GameState':
        id = str(uuid.uuid4())
        return GameState(id=id, players=players)
    
    def register_events(self) -> None:
        register_event_listener(event_type=EventType.GAME_STATE_TICK, game_state_id=self.id, listener=self.tick_up)

    async def tick_up(self) -> EventResponse:
        self.event_tick += 1
        return EventResponse.success()