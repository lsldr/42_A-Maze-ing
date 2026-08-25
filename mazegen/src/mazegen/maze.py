from mazegen.cell import Cell, Wall
from mazegen.util import Point


class MazeError(Exception):
    """Error class for when somethin is not right with maze object"""


class Maze:
    def __init__(self,
                 size: Point,
                 entry: Point,
                 exit: Point) -> None:
        if (entry[0] < 0 or entry[1] < 0 or
            entry[0] >= size[0] or entry[1] >= size[1]):
            raise ValueError("Entry point outside maze structure")
        if (exit[0] < 0 or exit[1] < 0 or
            exit[0] >= size[0] or exit[1] >= size[1]):
            raise ValueError("Exit point outside maze structure")
        self._size = size
        self._entry = entry
        self._exit = exit
        self._maze = [[Cell() for _ in range(size[1])] for _ in range(size[0])]

    @property
    def size(self) -> tuple[int, int]:
        """Size of the maze

        Returns:
            width (int) and height (int)
        """
        return self._size

    @property
    def entry(self) -> Point:
        return self._entry

    @property
    def exit(self) -> Point:
        return self._exit

    def in_bounds(self, pos: Point) -> bool:
        return (pos.x >= 0 and pos.y >= 0 and
            pos.x < self._size.x and pos.y < self._size.y)

    def is_ready(self) -> bool:
        for row in self._maze:
            for cell in row:
                if cell.lock:
                    continue
                if cell.walls == Wall.ALL:
                    return False
        return True

    def is_valid(self) -> None:
        """Returns nothing, raises MazeError if maze is invalid"""
        # TODO: check for "rooms" - spaces that are at least 2x2
        for x, row in enumerate(self._maze):
            for y, cell in enumerate(row):
                match ~cell.walls:
                    case Wall.NORTH:
                        if y == 0:
                            raise MazeError("Wall missing on the "
                                            "north edge of the maze")
                    case Wall.SOUTH:
                        if y == self.size[1] - 1:
                            raise MazeError("Wall missing on the "
                                            "south edge of the maze")
                    case Wall.WEST:
                        if x == 0:
                            raise MazeError("Wall missing on the "
                                            "west edge of the maze")
                    case Wall.SOUTH:
                        if x == self.size[0] - 1:
                            raise MazeError("Wall missing on the "
                                            "east edge of the maze")
                for dir in [Wall.NORTH, Wall.WEST]:
                    opposite = dir.opposite()
                    dx, dy = dir.get_direction()
                    if x + dx < 0 or y + dy < 0:
                        continue
                    if (dir not in cell.walls and
                        opposite in self._maze[x + dx][y + dy].walls):
                        err = (f"Wall discrpancy between cell {x}, {y}"
                               f" and {x + dx}, {y + dy}")
                        raise MazeError(err)

    def clean_visited(self) -> None:
        for row in self._maze:
            for cell in row:
                cell.visited = False

    def get_cell(self, pos: Point) -> Cell:
        if not self.in_bounds(pos):
            raise ValueError("Position outside the maze")
        return self._maze[pos.x][pos.y]

    def get_neighbors_in_bounds(self, pos: Point) -> list[Wall]:
        if not self.in_bounds(pos):
            raise ValueError("Position outside the maze")
        possible = []
        x, y = pos
        for side in Wall.ALL:
            dx, dy = side.get_direction()
            if self.in_bounds(Point(x + dx, y + dy)):
                possible.append(side)
        return possible

    def try_open_wall(self, pos: Point, side: Wall) -> bool:
        x, y = pos
        if not self.in_bounds(pos):
            raise ValueError("Position outside the maze")
        dx, dy  = side.get_direction()
        if abs(dx + dy) != 1:
            raise ValueError("side need to be only one of the direction")
        nx, ny = x + dx, y + dy
        if self._maze[pos[0]][pos[1]].lock or self._maze[nx][ny].lock:
            return False
        # Checked above if safe
        self._maze[x][y].open_wall(side)
        self._maze[nx][ny].open_wall(side.opposite())
        return True

    def __str__(self) -> str:
        ret = ""
        for row in self._maze:
            for cell in row:
                ret += str(cell)
            ret += "\n"
        ret += f"\n{self.entry[0]},{self.entry[1]}\n"
        ret += f"{self.exit[0]},{self.exit[0]}\n"
        return ret
