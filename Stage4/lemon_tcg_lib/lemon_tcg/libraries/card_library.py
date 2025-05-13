from typing import Optional
from lemon_tcg.entities.card import Card
from lemon_tcg.utils.file_operations import construct_path, files_in_directory

CARDS_DIRECTORY_PATH = construct_path("lemon_tcg/data/cards")

class CardLibrary():
    _instance = None

    def __init__(self) -> None:
        if CardLibrary._instance is not None:
            raise RuntimeError("Tried to initialize multiple instances of CardLibrary.")
        self.cards: dict[str, Card] = {}
        self.refresh()
    
    @staticmethod
    def _load_card(id: str) -> 'Card':
        try:
            card = Card.load_from_id(id=id)
        except Exception as e:
            raise RuntimeError(f"An error occured while loading card '{id}': {e}")
        return card

    @staticmethod
    def get_instance() -> 'CardLibrary':
        if CardLibrary._instance is None:
            CardLibrary._instance = CardLibrary()
        return CardLibrary._instance
    
    def refresh(self) -> None:
        cards = {}
        files = files_in_directory(path=CARDS_DIRECTORY_PATH, suffix=".json")
        ids = [file[:-5] for file in files]
        for id in ids:
            cards[id] = self._load_card(id=id)
        self.cards = cards

    def get_by_id(self, id: str) -> Optional[Card]:
        self.refresh()
        id = id.lower()
        return self.cards.get(id, None)