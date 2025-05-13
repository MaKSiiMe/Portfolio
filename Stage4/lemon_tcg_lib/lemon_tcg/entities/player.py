from pydantic import BaseModel

class Player(BaseModel):
    id: str
    index: int
    card_count: int
    display_name: str
    _dispatch_id: str = ""

    def register_events(self, dispatch_id: str) -> None:
        self._dispatch_id = dispatch_id