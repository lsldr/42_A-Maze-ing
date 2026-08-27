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

        x_size = self.maze.size.x
        y_size = self.maze.size.y
        for x in range(x_size):
            for y in range(y_size):
                p = Point(x, y)
                if not self.maze.grid[p.x][p.y].lock:
                    for w in [Wall.EAST, Wall.SOUTH]:
                        if (
                            x == x_size - 1
                            and w == Wall.EAST
                            or y == y_size - 1
                            and w == Wall.SOUTH
                        ):
                            continue
                        wall_list.append(tuple(Point(x, y), w))

        return wall_list

    def get_cell_dset(self) -> DisjointSet:

        cells_dset = DisjointSet(
            [
                {i: c}
                for i in range(self.maze.size.x * self.maze.size.y)
                for c in [point for point in self.maze.grid]
            ]
        )

        return cells_dset
