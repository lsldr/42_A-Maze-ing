from mazegen.cell import Wall
from mazegen.generator.maze_generator import Maze_Generator
from mazegen.maze import Maze
from mazegen.util import Point
from random import Random


class DFS_gen(Maze_Generator):
    def __init__(self, maze: Maze, rand: Random, perfect: bool = True) -> None:
        super().__init__(maze, rand, perfect)
        self._stack: list[Point] = []
        # Pre-populate visited with pattern cells so DFS ignores them
        self._visited: set[Point] = set(self.maze.pattern_cells)

    def next(self) -> tuple[Maze, Point | None, list[Point] | None]:
        # 1. Initialize DFS from Entry
        if not self._stack and self.maze.entry not in self._visited:
            pos = self.maze.entry
            self._visited.add(pos)
            self.maze.get_cell(pos).visited = True
            self._stack.append(pos)
            return (self.maze, pos, self._stack.copy())

        # Generation complete or stack emptied
        if not self._stack:
            return (self.maze, None, [])

        pos = self._stack[-1]
        x, y = pos

        # 2. Find valid, unvisited, non-pattern neighbors
        neighbors: list[tuple[Wall, Point]] = []
        for side in [Wall.NORTH, Wall.EAST, Wall.SOUTH, Wall.WEST]:
            dx, dy = side.get_direction()
            npos = Point(x + dx, y + dy)
            if self.maze.in_bounds(npos) and npos not in self._visited:
                neighbors.append((side, npos))

        if neighbors:
            # Pick a random neighbor and carve a wall
            side, npos = self._rand.choice(neighbors)
            if self.maze.try_open_wall(pos, side):
                self._visited.add(npos)
                self.maze.get_cell(npos).visited = True
                self._stack.append(npos)
            return (self.maze, npos, self._stack.copy())
        else:
            # Backtrack from a dead end
            # Then loook for the prev cell's neighbors if it's in stack
            self._stack.pop()
            return (self.maze, pos, self._stack.copy())

    def finish(self) -> Maze:
        """Run DFS to completion and add loops if non-perfect."""
        while not self.maze.is_ready() and (
            self._stack or self.maze.entry not in self._visited
        ):
            self.next()

        if not self._perfect:
            self._add_loops()

        return self.maze

    def _add_loops(self, loop_factor: float = 0.05) -> None:
        """Randomly opens additional walls while avoiding pattern cells."""
        extra_walls = int(self.maze.size.x * self.maze.size.y * loop_factor)
        for _ in range(extra_walls):
            rx = self._rand.randint(0, self.maze.size.x - 1)
            ry = self._rand.randint(0, self.maze.size.y - 1)
            pos = Point(rx, ry)
            if pos in self.maze.pattern_cells:
                continue

            side = self._rand.choice(
                [Wall.NORTH, Wall.EAST, Wall.SOUTH, Wall.WEST]
            )
            self.maze.try_open_wall(pos, side)
