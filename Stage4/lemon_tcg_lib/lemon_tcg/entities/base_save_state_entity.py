from pydantic import BaseModel
from typing import ClassVar
from lemon_tcg.utils.file_operations import file_to_string, string_to_file, file_exists

class BaseSaveStateEntity(BaseModel):
    FILE_PATH: ClassVar = ""

    def save_state(self) -> None:
        data = self.model_dump_json()
        string_to_file(file_path=self.FILE_PATH, data=data)

    @classmethod
    def load_state(cls):
        if not file_exists(cls.FILE_PATH):
            data = "{}"
        else:
            data = file_to_string(file_path=cls.FILE_PATH)
        return cls.model_validate_json(json_data=data)