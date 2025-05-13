from typing import Optional
from lemon_tcg.entities.game_state import GameState
from lemon_tcg.utils.file_operations import construct_path, files_in_directory

GAME_STATE_DIRECTORY_PATH = construct_path("lemon_tcg/data/save/games")

class GameStateLibrary():
    _instance = None

    def __init__(self) -> None:
        if GameStateLibrary._instance is not None:
            raise RuntimeError("Tried to initialize multiple instances of GameStateLibrary.")
        self.game_states: dict[str, GameState] = {}
        self.refresh()

    @staticmethod
    def _load_game_state(id: str) -> 'GameState':
        try:
            game_state = GameState.load_state(id=id)
        except Exception as e:
            raise RuntimeError(f"An error occured while loading game state '{id}': {e}")
        return game_state
        
    @staticmethod
    def get_instance() -> 'GameStateLibrary':
        if GameStateLibrary._instance is None:
            GameStateLibrary._instance = GameStateLibrary()
        return GameStateLibrary._instance
    
    def refresh(self) -> None:
        game_states = {}
        files = files_in_directory(path=GAME_STATE_DIRECTORY_PATH, suffix=".json")
        ids = [file[:-5] for file in files]
        for id in ids:
            game_states[id] = self._load_game_state(id=id)
        self.game_states = game_states
    
    def get_by_id(self, id: str) -> Optional[GameState]:
        self.refresh()
        id = id.lower()
        return self.game_states.get(id, None)