from lemon_tcg.constants.language import Language
from lemon_tcg.entities.config import Config

class Context():
    _instance = None

    def __init__(self) -> None:
        if Context._instance is not None:
            raise RuntimeError("Tried to initialize multiple instances of Context.")
        self.config = Config.load_state()
        
    @staticmethod
    def get_instance() -> 'Context':
        if Context._instance is None:
            Context._instance = Context()
        return Context._instance
    
    @property
    def language(self) -> Language:
        return self.config.language
    
    def clear_config(self) -> None:
        self.config = Config()

    def reset_config(self) -> None:
        self.clear_config()
        self.config.save_state()