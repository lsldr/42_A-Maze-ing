from mazegen import Wall
from mazegen.generator import MazeGenerator
from mazegen.maze import Maze
from mazegen.util import Point
from random import Random


class WilsonsGen(MazeGenerator):
    def __init__(
        self, maze: Maze, rand: Random, perfect: bool = False
    ) -> None:
        super().__init__(maze, rand, perfect)
        self._avalible = {Point(x, y) for x in range(maze.size.x)
             for y in range(maze.size.y)}
        pos = rand.choice(list(self._avalible))
        maze.get_cell(pos).visited = True
        self._avalible.discard(pos)
        self._avalible.difference_update(self.maze.pattern_cells)
        self._path: list[Point] = []

    def next(self) -> tuple[Maze, Point | None, list[Point] | None]:
        if not self._avalible:
            return self.maze, None, None

        if not self._path:
            self._path.append(self._rand.choice(list(self._avalible)))
            return self.maze, self._path[0], self._path.copy()

        last = self._path[-1]

        # Find valid neigbors
        neighbors: list[Point] = []
        for side in Wall.ALL:
            dx, dy = side.get_direction()
            npos = Point(last.x + dx, last.y + dy)
            if self.maze.in_bounds(npos) and not self.maze.get_cell(npos).lock:
                neighbors.append(npos)

        next = self._rand.choice(neighbors)

        # next created a loop keep first
        if next in self._path:
            first = self._path[0]
            while self._path.pop() != next:
                pass
            if len(self._path) == 0:
                self._path.append(first)
            return self.maze, self._path[0], self._path.copy()

        # next is previously visited path
        if self.maze.get_cell(next).visited:
            p1 = next
            while len(self._path):
                p2: Point = self._path.pop()
                dx, dy = p1.x - p2.x, p1.y - p2.y
                side = Wall.from_direction(Point(dx, dy))
                cell = self.maze.get_cell(p2)
                self.maze.try_open_wall(p2, side)
                cell.visited = True
                self._avalible.discard(p2)
                p1 = p2
            return self.maze, None, None

        self._path.append(next)
        return self.maze, self._path[0], self._path.copy()
