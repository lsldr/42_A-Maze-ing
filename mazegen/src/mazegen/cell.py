from enum import Flag
from mazegen.util import Point


class Wall(Flag):
    NONE = 0
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    ALL = NORTH | EAST | SOUTH | WEST

    def get_direction(self) -> Point:
        x = 0
        y = 0
        x += 1 if self.EAST in self else 0
        x -= 1 if self.WEST in self else 0
        y += 1 if self.SOUTH in self else 0
        y -= 1 if self.NORTH in self else 0
        return Point(x, y)

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
                    return "a"
                case 11:
                    return "b"
                case 12:
                    return "c"
                case 13:
                    return "d"
                case 14:
                    return "e"
                case 15:
                    return "f"
        return str(self.value)


class Cell:
    def __init__(self) -> None:
        self._walls: Wall = Wall.ALL
        self.lock = False
        self.visited = False

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
