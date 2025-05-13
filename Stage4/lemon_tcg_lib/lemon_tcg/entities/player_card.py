from pydantic import BaseModel

# A card that is currently played in the game, including all the important data associated with that
class GameCard(BaseModel):
    id: str
    owner_index: int
    meta_data: dict = {}