from typing import Self
from enum import Flag, auto


class Wall(Flag):
    NONE = 0
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()
    ALL = NORTH | EAST | SOUTH | WEST

    def get_direction(self) -> tuple[int, int]:
        x = 0
        y = 0
        x += 1 if self.EAST in self else 0
        x -= 1 if self.WEST in self else 0
        y += 1 if self.SOUTH in self else 0
        y -= 1 if self.NORTH in self else 0
        return (x, y)

    def opposite(self) -> Wall:
        ret = self.NONE
        match self:
            case self.EAST:
                ret |= self.WEST
            case self.WEST:
                ret |= self.EAST
            case self.NORTH:
                ret |= self.SOUTH
            case self.SOUTH:
                ret |= self.NORTH
        return ret

    def __str__(self) -> str:
        if self.value > 9:
            match self.value:
                case 10:
                    return "A"
                case 11:
                    return "B"
                case 12:
                    return "C"
                case 13:
                    return "D"
                case 14:
                    return "E"
                case 15:
                    return "F"
        return str(self.value)


class Cell:
    def __init__(self) -> None:
        self._walls: Wall = Wall.ALL
        self.lock = False

    def open_wall(self, side: Wall) -> None:
        if not self.lock:
            self._walls = self._walls & ~side
        else:
            raise ValueError("Trying to delete a wall in a locked cell")

    @property
    def walls(self) -> Wall:
        return self._walls

    def __str__(self) -> str:
        return str(self._walls)
