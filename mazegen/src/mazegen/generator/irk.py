from mazegen.cell import Wall
from mazegen.generator.maze_generator import Maze_Generator
from mazegen.maze import Maze
from mazegen.util import Point
from random import Random
from disjoint_set import DisjointSet


class IRK_Gen(Maze_Generator):
    def __init__(
        self, maze: Maze, rand: Random, perfect: bool = False
    ) -> None:
        super().__init__(maze, rand, perfect)
        self._walls_list = self.make_wall_list()
        self._cells_dset = self.get_cell_dset()

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

    def get_cell_dset(self) -> DisjointSet:
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

        return DisjointSet.from_iterable(points_list)
