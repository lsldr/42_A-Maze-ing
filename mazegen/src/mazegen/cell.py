from enum import IntFlag, auto


class Wall(IntFlag):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()
    ALL = NORTH | EAST | SOUTH | WEST


class Cell:
    def __init__(self) -> None:
        self._walls: Wall = Wall.ALL
        self.lock = False

    def del_wall(self, side: Wall) -> None:
        if not self.lock:
            self._walls = self._walls & ~side
        else:
            raise ValueError("Trying to delete a wall in a locked cell")

    def get_walls(self) -> Wall:
        return self._walls
