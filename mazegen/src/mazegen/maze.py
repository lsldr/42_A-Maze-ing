from mazegen.cell import Cell, Wall
from mazegen.util import Point


class MazeError(Exception):
    """Error class for when something is not right with maze object"""


class Maze:
    def __init__(
        self,
        size: Point,
        entry: Point,
        exit: Point,
        pattern_cells: set[tuple[int, int]] | set[Point] | None = None,
    ) -> None:
        if not (0 <= entry.x < size.x and 0 <= entry.y < size.y):
            raise ValueError("Entry point outside maze structure")
        if not (0 <= exit.x < size.x and 0 <= exit.y < size.y):
            raise ValueError("Exit point outside maze structure")

        self._size = size
        self._entry = entry
        self._exit = exit
        self._maze = [[Cell() for _ in range(size.y)] for _ in range(size.x)]

        # Store pattern cells and lock them
        self._pattern_cells: set[Point] = {
            Point(*p) for p in (pattern_cells or set())
        }
        for p in self._pattern_cells:
            if self.in_bounds(p):
                self.get_cell(p).lock = True

    @property
    def size(self) -> Point:
        return self._size

    @property
    def entry(self) -> Point:
        return self._entry

    @property
    def exit(self) -> Point:
        return self._exit

    @property
    def pattern_cells(self) -> set[Point]:
        return self._pattern_cells

    @property
    def grid(self) -> list[list[Cell]]:
        return self._maze

    def in_bounds(self, pos: Point) -> bool:
        return 0 <= pos.x < self._size.x and 0 <= pos.y < self._size.y

    def get_cell(self, pos: Point) -> Cell:
        if not self.in_bounds(pos):
            raise ValueError(f"Position {pos} outside the maze")
        return self._maze[pos.x][pos.y]

    def try_open_wall(self, pos: Point, side: Wall) -> bool:
        """Opens  wall between pos and pos + side.

        Returns False if out of bounds or if either cell is locked.
        """
        if not self.in_bounds(pos):
            return False
        dx, dy = side.get_direction()
        npos = Point(pos.x + dx, pos.y + dy)
        if not self.in_bounds(npos):
            return False

        cell = self.get_cell(pos)
        ncell = self.get_cell(npos)

        # Protect locked (pattern) cells on both sides
        if cell.lock or ncell.lock:
            return False

        cell.open_wall(side)
        ncell.open_wall(side.opposite())
        return True

    def is_ready(self) -> bool:
        """Check if all non-locked cells have been reached."""
        for x in range(self._size.x):
            for y in range(self._size.y):
                cell = self._maze[x][y]
                if cell.lock:
                    continue
                if cell.walls == Wall.ALL:
                    return False
        return True
