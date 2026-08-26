from mazegen.cell import Wall
from mazegen.generator.maze_generator import Maze_Generator
from mazegen.maze import Maze
from mazegen.util import Point
from random import Random


class IRK_Gen(Maze_Generator):
    def __init__(
        self, maze: Maze, rand: Random, perfect: bool = False
    ) -> None:
        super().__init__(maze, rand, perfect)

    def next(self) -> tuple[Maze, Point | None, list[Point] | None]: