from __future__ import annotations

from enum import Flag
from mazegen.util import Point
from typing import Iterable


class Wall(Iterable, Flag):
    """Bitmask representing walls of a maze cell."""

    NONE = 0
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    ALL = NORTH | EAST | SOUTH | WEST

    def get_direction(self) -> Point:
        """Get the coordinate delta corresponding to the wall direction.

        Returns:
            Point: Relative delta (dx, dy) for the wall direction.
        """
        x = 0
        y = 0
        x += 1 if self.EAST in self else 0
        x -= 1 if self.WEST in self else 0
        y += 1 if self.SOUTH in self else 0
        y -= 1 if self.NORTH in self else 0
        return Point(x, y)

    @classmethod
    def from_direction(cls, dir: Point) -> Wall:
        """Determine wall flag from a directional coordinate vector.

        Args:
            dir (Point): Cardinal direction vector.

        Returns:
            Wall: Corresponding Wall enum flag.

        Raises:
            ValueError: If direction is not a valid cardinal direction.
        """
        sides = [cls.WEST, cls.EAST, cls.NORTH, cls.SOUTH]
        for w in sides:
            if w.get_direction() == dir:
                return w
        raise ValueError("Function only accepts cardinal directions")

    def opposite(self) -> Wall:
        """Get the opposite wall direction.

        Returns:
            Wall: Wall flag representing the opposite direction.
        """
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
        """Get hexadecimal character representation of wall bitmask.

        Returns:
            str: Single hexadecimal character representing the wall value.
        """
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
    """Cell in a maze grid.

    Attributes:
        lock (bool): If True, cell is locked and cannot be modified.
        visited (bool): If True, cell has been visited.
    """

    def __init__(self) -> None:
        """Initialize an unvisited cell with all walls intact."""
        self._walls: Wall = Wall.ALL
        self.lock = False
        self.visited = False

    def open_wall(self, side: Wall) -> None:
        """Open selected wall side if cell is not locked.

        Args:
            side (Wall): The wall side to remove.

        Raises:
            ValueError: If trying to remove a wall in a locked cell.
        """
        if not self.lock:
            self._walls = self._walls & ~side
        else:
            raise ValueError("Trying to delete a wall in a locked cell")

    @property
    def walls(self) -> Wall:
        """Wall: Bitmask representing remaining walls of this cell."""
        return self._walls

    def __str__(self) -> str:
        """Get string representation of cell walls.

        Returns:
            str: Hexadecimal character representing cell walls.
        """
        return str(self._walls)
