from random import Random
from mazegen.generator.maze_generator import Maze_Generator
from mazegen.maze import Maze

class DFS_gen(Maze_Generator):
    def __init__(self,
                 maze: Maze, rand: Random, perfect: bool = False) -> None:
        super().__init__(maze, rand, perfect)
        self._path: list[tuple[int, int]] = []

    def next(self) -> tuple[Maze,
                            tuple[int, int] | None,
                            list[tuple[int, int]] | None]:
        if not self._path:
            x = self._rand.randint(0, self.maze.size[0] - 1)
            y = self._rand.randint(0, self.maze.size[1] - 1)
            pos = (x, y)
            self.maze.get_cell(pos).visited = True
            self._path.append(pos)
            return (self.maze, None, self._path.copy())

        pos = self._path[-1]
        x, y = pos
        cell = self.maze.get_cell(pos)
        possible = [x for x in self.maze.get_neighbors_in_bounds(pos)
                   if x in cell.walls]
        neighbors = []
        for n in possible:
            dx, dy = n.get_direction()
            if not self.maze.get_cell((x + dx, y + dy)).lock:
                neighbors.append(n)

        if not neighbors:
            self._path.pop()
            return (self.maze, None, self._path.copy())

        move = self._rand.choice(neighbors)
        dx, dy = move.get_direction()
        if self.maze.try_open_wall(pos, move):
            self._path.append((x + dx, y + dy))

        return (self.maze, None, self._path.copy())
