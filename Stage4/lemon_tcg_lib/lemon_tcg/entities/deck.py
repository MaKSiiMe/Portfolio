from lemon_tcg.entities.base_save_state_entity_group import BaseSaveStateEntityGroup
from lemon_tcg.utils.file_operations import construct_path

class Deck(BaseSaveStateEntityGroup):
    FILE_PATH = construct_path("lemon_tcg/data/save/decks/{id}.json")
    name: str = "No Name"
    cards: dict[str, int] = {}