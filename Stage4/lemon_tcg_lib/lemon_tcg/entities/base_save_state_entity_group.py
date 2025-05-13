from pydantic import BaseModel
from typing import ClassVar
from lemon_tcg.utils.file_operations import construct_path, file_to_string, string_to_file, file_exists

class BaseSaveStateEntityGroup(BaseModel):
    FILE_PATH: ClassVar = construct_path("lemon_tcg/{id}.json")
    id: str = "unknown"

    @classmethod
    def get_file_path(cls, id: str) -> str:
        return cls.FILE_PATH.format(id=id)

    def save_state(self) -> None:
        data = self.model_dump_json()
        string_to_file(file_path=self.get_file_path(id=self.id), data=data)

    @classmethod
    def load_state(cls, id: str = "unknown"):
        if not file_exists(cls.get_file_path(id=id)):
            data = "{}"
        else:
            data = file_to_string(file_path=cls.get_file_path(id=id))
        return cls.model_validate_json(json_data=data)