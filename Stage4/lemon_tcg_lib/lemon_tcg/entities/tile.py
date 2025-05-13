from pydantic import BaseModel
from lemon_tcg.constants.tile_state import TileState

class Tile(BaseModel):
    state: TileState = TileState.VOID