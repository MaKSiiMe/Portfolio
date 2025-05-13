from pydantic import BaseModel
from lemon_tcg.utils.validator import validate_user_index

# Global coordinates start in the top left
# User coordinates start in the top left of their respective part of the board from their POV
# User 0 is at the bottom with regular POV
# User 1 is at the top with inverted POV
class Coordinates(BaseModel):
    x: int
    y: int

    def user_to_global(self, user_index: int, board_height: int, board_width: int) -> 'Coordinates':
        validate_user_index(user_index=user_index)
        half_height = board_height // 2
        if user_index == 0:
            x = self.x
            y = half_height + self.y
        else:
            x = board_width - self.x - 1
            y = half_height - self.y - 1
        return Coordinates(x=x, y=y)
    
    def global_to_user(self, user_index: int, board_height: int, board_width: int) -> 'Coordinates':
        validate_user_index(user_index=user_index)
        half_height = board_height // 2
        if user_index == 0:
            x = self.x
            y = self.y - half_height
        else:
            x = board_width - self.x - 1
            y = half_height - self.y - 1
        return Coordinates(x=x, y=y)
    
    def global_to_tile_index(self, board_width: int) -> int:
        return board_width * self.y + self.x
    
    def user_to_tile_index(self, user_index: int, board_height: int, board_width: int) -> int:
        global_coordinates = self.user_to_global(user_index=user_index, board_height=board_height, board_width=board_width)
        return global_coordinates.global_to_tile_index(board_width=board_width)
    
