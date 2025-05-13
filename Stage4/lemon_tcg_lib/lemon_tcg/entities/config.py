from lemon_tcg.constants.language import Language
from lemon_tcg.entities.base_save_state_entity import BaseSaveStateEntity
from lemon_tcg.utils.file_operations import construct_path

class Config(BaseSaveStateEntity):
    FILE_PATH = construct_path("lemon_tcg/data/save/config.json")
    language: Language = Language.ENGLISH
    default_board_height: int = 6
    default_board_width: int = 5

    def set_language(self, language: Language) -> None:
        if not isinstance(language, Language):
            raise RuntimeError(f"Tried to change config language, but given language is invalid.")
        self.language = language