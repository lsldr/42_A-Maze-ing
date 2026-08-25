from mazegen.generator.maze_generator import Maze_Generator
from mazegen.maze import Maze
from mazegen.util import Point
from random import Random


class DFS_gen(Maze_Generator):
    def __init__(
        self, maze: Maze, rand: Random, perfect: bool = False
    ) -> None:
        super().__init__(maze, rand, perfect)
        self._path: list[Point] = []

    def next(self) -> tuple[Maze, Point | None, list[Point] | None]:
        if not self._path:
            x = self._rand.randint(0, self.maze.size[0] - 1)
            y = self._rand.randint(0, self.maze.size[1] - 1)
            pos = Point(x, y)
            self.maze.get_cell(pos).visited = True
            self._path.append(pos)
            return (self.maze, None, self._path.copy())

        pos = self._path[-1]
        x, y = pos
        cell = self.maze.get_cell(pos)
        cell.visited = True
        possible = [
            x
            for x in self.maze.get_neighbors_in_bounds(pos)
            if x in cell.walls
        ]
        neighbors = []
        for n in possible:
            dx, dy = n.get_direction()
            c = self.maze.get_cell(Point(x + dx, y + dy))
            if not (c.lock or c.visited):
                neighbors.append(n)

        if not neighbors:
            self._path.pop()
            return (self.maze, None, self._path.copy())

        move = self._rand.choice(neighbors)
        dx, dy = move.get_direction()
        if self.maze.try_open_wall(pos, move):
            self._path.append(Point(x + dx, y + dy))

        return (self.maze, None, self._path.copy())
