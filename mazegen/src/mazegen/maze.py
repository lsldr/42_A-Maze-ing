from mazegen.cell import Cell, Wall
from mazegen.util import Point


class MazeError(Exception):
    """Exception raised for invalid maze state or operations."""


class Maze:
    """Representation of a grid-based maze.

    Attributes:
        path (list[Point]): Shortest path between entry and exit points.
    """

    def __init__(
        self,
        size: Point,
        entry: Point | None = None,
        exit: Point | None = None,
        pattern_cells: set[tuple[int, int]] | set[Point] | None = None,
    ) -> None:
        """Initialize the maze grid and boundaries.

        Args:
            size (Point): Dimensions (width, height) of the maze.
            entry (Point, optional): Coordinates of the entry cell.
            exit (Point, optional): Coordinates of the exit cell.
            pattern_cells (set[tuple[int, int]] | set[Point],
                optional): Coordinates of immutable locked pattern cells.
                Defaults to None.

        Raises:
            ValueError: If entry or exit coordinates are outside maze bounds.
        """
        if not entry:
            entry = Point(0, 0)
        if not exit:
            exit = Point(size.x - 1, size.y - 1)
        if not (0 <= entry.x < size.x and 0 <= entry.y < size.y):
            raise ValueError("Entry point outside maze structure")
        if not (0 <= exit.x < size.x and 0 <= exit.y < size.y):
            raise ValueError("Exit point outside maze structure")

        self._size = size
        self._entry = entry
        self._exit = exit
        self._maze = [[Cell() for _ in range(size.y)] for _ in range(size.x)]
        self.path: list[Point] = []  # To hold the shortest path

        # Store pattern cells and lock them
        self._pattern_cells: set[Point] = {
            Point(*p) for p in (pattern_cells or set())
        }
        for p in self._pattern_cells:
            if self.in_bounds(p):
                self.get_cell(p).lock = True

    @property
    def size(self) -> Point:
        """Point: Dimensions of the maze grid."""
        return self._size

    @property
    def entry(self) -> Point:
        """Point: Entry coordinate of the maze."""
        return self._entry

    @property
    def exit(self) -> Point:
        """Point: Exit coordinate of the maze."""
        return self._exit

    @property
    def pattern_cells(self) -> set[Point]:
        """set[Point]: Set of immutable pattern cell coordinates."""
        return self._pattern_cells

    @property
    def grid(self) -> list[list[Cell]]:
        """list[list[Cell]]: 2D grid containing all maze cells."""
        return self._maze

    def __str__(self) -> str:
        """Return the maze formatted as hexadecimal rows with coordinates.

        Returns:
            str: Hexadecimal maze representation followed by entry, exit, path.
        """
        lines = []
        # Iterate row by row (y first, then x)
        for y in range(self._size.y):
            row_str = "".join(
                str(self._maze[x][y]) for x in range(self._size.x)
            )
            lines.append(row_str)
        # Append empty line and coordinates as required by the subject
        lines.append("")
        lines.append(f"{self.entry.x},{self.entry.y}")
        lines.append(f"{self.exit.x},{self.exit.y}")
        lines.append(f"{self.path_to_directions(self.path)}")
        return "\n".join(lines)

    def in_bounds(self, pos: Point) -> bool:
        """Check if a coordinate is within the maze bounds.

        Args:
            pos (Point): Position coordinate to test.

        Returns:
            bool: True if position is within bounds, False otherwise.
        """
        return 0 <= pos.x < self._size.x and 0 <= pos.y < self._size.y

    def get_cell(self, pos: Point) -> Cell:
        """Get cell at specified coordinates.

        Args:
            pos (Point): Position coordinate of the cell.

        Returns:
            Cell: Cell instance at the given position.

        Raises:
            IndexError: If position is outside maze bounds.
        """
        if not self.in_bounds(pos):
            raise IndexError(f"Position {pos} outside the maze")
        return self._maze[pos.x][pos.y]

    def try_open_wall(self, pos: Point, side: Wall) -> bool:
        """Open a shared wall between a cell and its neighbor.

        Args:
            pos (Point): Position of the source cell.
            side (Wall): Wall side to open.

        Returns:
            bool: True if wall was successfully opened, False if out of bounds
                or if either cell is locked.
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

    def count_open_passages(self, pos: Point) -> int:
        """Count the number of open passages for a given cell.

        Args:
            pos (Point): Coordinate of the cell to inspect.

        Returns:
            int: Number of open cardinal passages (0 to 4).
        """
        cell = self.get_cell(pos)
        if cell.lock:
            return 0
        return sum(
            1
            for side in [Wall.NORTH, Wall.EAST, Wall.SOUTH, Wall.WEST]
            if side not in cell.walls
        )

    def _is_3x3_window_open(self, x0: int, y0: int) -> bool:
        """Check if a 3x3 block at (x0, y0) has all internal walls open.

        Args:
            x0 (int): Top-left X coordinate of the 3x3 block.
            y0 (int): Top-left Y coordinate of the 3x3 block.

        Returns:
            bool: True if the 3x3 block forms an open room, False otherwise.
        """
        for x in range(x0, x0 + 3):
            for y in range(y0, y0 + 3):
                pos = Point(x, y)
                if not self.in_bounds(pos) or self.get_cell(pos).lock:
                    return False
                # Check horizontal internal wall to the EAST
                if x < x0 + 2 and Wall.EAST in self.get_cell(pos).walls:
                    return False
                # Check vertical internal wall to the SOUTH
                if y < y0 + 2 and Wall.SOUTH in self.get_cell(pos).walls:
                    return False
        return True

    def would_create_3x3_room(self, pos: Point, side: Wall) -> bool:
        """Simulate opening a wall and check if it creates an open 3x3 room.

        Args:
            pos (Point): Position of the source cell.
            side (Wall): Wall side to test.

        Returns:
            bool: True if removing the wall would create a 3x3 open room.
        """
        dx, dy = side.get_direction()
        npos = Point(pos.x + dx, pos.y + dy)
        if not self.in_bounds(npos) or self.get_cell(npos).lock:
            return False

        # Temporarily open the wall
        self.get_cell(pos).open_wall(side)
        self.get_cell(npos).open_wall(side.opposite())

        # Check all 3x3 windows covering both pos and npos
        min_x = max(0, max(pos.x, npos.x) - 2)
        max_x = min(self.size.x - 3, min(pos.x, npos.x))
        min_y = max(0, max(pos.y, npos.y) - 2)
        max_y = min(self.size.y - 3, min(pos.y, npos.y))

        creates_room = False
        for x0 in range(min_x, max_x + 1):
            for y0 in range(min_y, max_y + 1):
                if self._is_3x3_window_open(x0, y0):
                    creates_room = True
                    break
            if creates_room:
                break

        # Revert the temporary wall opening
        self.get_cell(pos)._walls |= side
        self.get_cell(npos)._walls |= side.opposite()

        return creates_room

    def is_ready(self) -> bool:
        """Check if all non-locked cells have at least one wall carved out.

        Returns:
            bool: True if every unlocked cell has at least one open wall.
        """
        for x in range(self._size.x):
            for y in range(self._size.y):
                cell = self._maze[x][y]
                if cell.lock:
                    continue
                if cell.walls == Wall.ALL:
                    return False
        return True

    @staticmethod
    def path_to_directions(path: list[Point]) -> str:
        """Convert a coordinate path into cardinal direction letters.

        Args:
            path (list[Point]): Sequential list of coordinate points.

        Returns:
            str: String of uppercase direction characters (e.g. 'NNEESW').
        """
        if len(path) < 2:
            return ""
        directions = []
        for i in range(len(path) - 1):
            curr, nxt = path[i], path[i + 1]
            dx, dy = nxt.x - curr.x, nxt.y - curr.y
            if dy == -1:
                directions.append("N")
            elif dx == 1:
                directions.append("E")
            elif dy == 1:
                directions.append("S")
            elif dx == -1:
                directions.append("W")
        return "".join(directions)
