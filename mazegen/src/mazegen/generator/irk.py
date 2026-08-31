from .maze_generator import MazeGenerator
from disjoint_set import DisjointSet
from mazegen.cell import Wall
from mazegen.maze import Maze
from mazegen.util import Point
from random import Random


class IRK_Gen(MazeGenerator):
    """Generate maze using Iterative Randomized Kruskal's algorithm.

    Attributes:
        maze (Maze): Maze object to be worked on.
    """

    def __init__(self, maze: Maze,
                 perfect: bool = False,
                 rand: float | str | Random | None = None
            ) -> None:
        """Initialize generator.

        Args:
            maze (Maze): Object to be worked on.
            rand (Random): Random number generator.
            perfect (bool): Defines if maze should have only
                one solution (True) or more (False).
        """
        super().__init__(maze, perfect, rand)
        self._walls_list = self._make_wall_list()
        self._cells_dset = self._get_cell_dset()
        self._cells_stack: list[Point] = []
        self._opened_set: set[Point] = set()

    def _make_wall_list(self) -> list[tuple[Point, Wall]]:
        """Create a randomized list of internal candidate walls.

        Returns:
            list[tuple[Point, Wall]]: List of tuples containing cell
                coordinates and candidate eastern/southern walls.
        """
        wall_list: list[tuple[Point, Wall]] = []

        for x in range(self.maze.size.x):
            for y in range(self.maze.size.y):
                point = Point(x, y)

                for side in (Wall.EAST, Wall.SOUTH):
                    dx, dy = side.get_direction()
                    neighbor = Point(x + dx, y + dy)

                    if (
                        self.maze.in_bounds(neighbor)
                        and not self.maze.get_cell(point).lock
                        and not self.maze.get_cell(neighbor).lock
                    ):
                        wall_list.append((point, side))

        self._rand.shuffle(wall_list)
        return wall_list

    def _get_cell_dset(self) -> DisjointSet[Point]:
        """Create a disjoint set collection for all unlocked cells.

        Returns:
            DisjointSet[Point]: Disjoint set structure tracking
                connected cells.
        """
        maze_grid = self.maze.grid
        maze_size = self.maze.size

        points_list = [
            Point(x, y)
            for x in range(maze_size.x)
            for y in range(maze_size.y)
            if not maze_grid[x][y].lock
        ]

        self._dset_size = len(points_list)

        return DisjointSet.from_iterable(points_list)

    def next(self) -> tuple[Maze, Point | None, list[Point] | None]:
        """Generate next step in maze generation.

        Returns:
            tuple[Maze, Point | None, list[Point] | None]: A tuple containing:
                - Maze: The modified maze instance.
                - Point | None: Optional coordinate of the last checked cell.
                - list[Point] | None: Optional stack of opened cell positions.
        """
        if not self._walls_list:
            return self.maze, None, self._cells_stack

        c_cell, c_wall = self._walls_list.pop()
        cx, cy = c_cell.x, c_cell.y

        dir = c_wall.get_direction()
        dx, dy = dir.x, dir.y
        n_cell = Point(cx + dx, cy + dy)

        if self._cells_dset.connected(c_cell, n_cell):
            return (self.maze, c_cell, self._cells_stack)

        if self.maze.try_open_wall(c_cell, c_wall):
            self._cells_dset.union(c_cell, n_cell)
            self._dset_size -= 1
            if c_cell not in self._opened_set:
                self._opened_set.add(c_cell)
                self._cells_stack.append(c_cell)
            if n_cell not in self._opened_set:
                self._opened_set.add(n_cell)
                self._cells_stack.append(n_cell)

        return self.maze, c_cell, self._cells_stack

    def finish(self) -> Maze:
        """Run generation to completion.

        Returns:
            Maze: The fully generated maze object.
        """
        while self._dset_size > 1 and self._walls_list:
            self.next()

        if not self._perfect:
            self._braid_maze()
        return self.maze
