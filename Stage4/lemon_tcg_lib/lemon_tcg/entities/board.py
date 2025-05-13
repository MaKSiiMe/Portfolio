from pydantic import BaseModel, computed_field
from lemon_tcg.event.type import EventType
from lemon_tcg.entities.coordinates import Coordinates
from lemon_tcg.entities.tile import Tile
from lemon_tcg.context import Context

CONTEXT = Context.get_instance()

class Board(BaseModel):
    height: int = CONTEXT.config.default_board_height
    width: int = CONTEXT.config.default_board_width
    tiles: list[Tile] = []
    _dispatch_id: str = ""

    @computed_field 
    @property
    def tile_count(self) -> int:
        return self.height * self.width
    
    def register_events(self, dispatch_id: str) -> None:
        self._dispatch_id = dispatch_id