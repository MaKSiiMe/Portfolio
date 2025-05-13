from typing import Optional
from lemon_tcg.entities.deck import Deck
from lemon_tcg.utils.file_operations import construct_path, files_in_directory

DECKS_DIRECTORY_PATH = construct_path("lemon_tcg/data/save/decks")

class DeckLibrary():
    _instance = None

    def __init__(self) -> None:
        if DeckLibrary._instance is not None:
            raise RuntimeError("Tried to initialize multiple instances of DeckLibrary.")
        self.decks: dict[str, Deck] = {}
        self.refresh()
    
    @staticmethod
    def _load_deck(id: str) -> 'Deck':
        try:
            deck = Deck.load_state(id=id)
        except Exception as e:
            raise RuntimeError(f"An error occured while loading deck '{id}': {e}")
        return deck

    @staticmethod
    def get_instance() -> 'DeckLibrary':
        if DeckLibrary._instance is None:
            DeckLibrary._instance = DeckLibrary()
        return DeckLibrary._instance
    
    def refresh(self) -> None:
        decks = {}
        files = files_in_directory(path=DECKS_DIRECTORY_PATH, suffix=".json")
        ids = [file[:-5] for file in files]
        for id in ids:
            decks[id] = self._load_deck(id=id)
        self.decks = decks

    def get_by_id(self, id: str) -> Optional[Deck]:
        self.refresh()
        id = id.lower()
        return self.decks.get(id, None)