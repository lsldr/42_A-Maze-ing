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

    def make_wall_list(self) -> list[tuple[Point, Wall]]:
        """Create a list with tuples containing points in grid bounds
        and walls from among the eastern and sotuhern ones to get internal
        walls only once. Edge walls can get there, but trying to open them
        would anyways prevent opening passages if `Perfect=True` in configs.

        Parameters:
        Instance of the IRK_Gen class (self)

        Returns:
        An ordered list with tuples of cells and eastern/southern walls"""

        wall_list: list[tuple[Point, Wall]] = []

        for x in range(self.maze.size.x):
            for y in range(self.maze.size.y):
                for w in [Wall.EAST, Wall.SOUTH]:
                    wall_list.append(tuple(Point(x, y), w))

        return wall_list
