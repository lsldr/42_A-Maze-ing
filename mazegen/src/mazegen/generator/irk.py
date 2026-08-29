from .maze_generator import MazeGenerator
from disjoint_set import DisjointSet
from mazegen.cell import Wall
from mazegen.maze import Maze
from mazegen.util import Point
from random import Random


class IRK_Gen(MazeGenerator):

    def __init__(
        self, maze: Maze, rand: Random, perfect: bool = False
    ) -> None:
        super().__init__(maze, rand, perfect)
        self._walls_list = self.make_wall_list()
        self._cells_dset = self.get_cell_dset()
        self._cells_stack: list[Point] = []

    def make_wall_list(self) -> list[tuple[Point, Wall]]:
        """Create a list with tuples containing points in grid bounds
        and walls from among the eastern and sotuhern ones to get internal
        walls only once.

        Parameters:
        Instance of the IRK_Gen class (self)

        Returns:
        An ordered list with tuples of cells and eastern/southern walls"""

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

    def get_cell_dset(self) -> DisjointSet[Point]:
        """Creates a disjoint set of all the cells that are not locked.
        A disjoint set is an array of sets that do not share any elements.
        When a union method is used on it, the two sets passed as parameters
        (initally, each set's representing element (like a dict key) is the
        single element contained in it) are made into 1 set where the
        representing element is chosen as the second parameter's value.
        The method to check if two elemenets are in the same set just compares
        those two elements' representing element.

        Parameters:
        Instance of the IRK_Gen class (self)

        Returns:
        A disjoint set collection with each set containing unlocked cells."""

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
        if not self._walls_list:
            return self.maze, None, None

        c_cell, c_wall = self._walls_list.pop()
        cx, cy = c_cell.x, c_cell.y

        dir = c_wall.get_direction()
        dx, dy = dir.x, dir.y
        n_cell = Point(cx + dx, cy + dy)

        self.maze.get_cell(c_cell).visited = True
        self.maze.get_cell(n_cell).visited = True

        self._cells_stack.append(c_cell)

        if self._cells_dset.connected(c_cell, n_cell):
            return (self.maze, c_cell, self._cells_stack)

        if self.maze.try_open_wall(c_cell, c_wall):
            self._cells_dset.union(c_cell, n_cell)
            self._dset_size -= 1

        return self.maze, c_cell, None

    def finish(self) -> Maze:
        """Run generation to completion.
        For Kruskal's, it's gotta be until the disjoint-set
        has the only set in it.

        Returns:
            ready maze
        """
        while self._dset_size > 1 and self._walls_list:
            self.next()

        if not self._perfect:
            self._braid_maze()
        return self.maze
