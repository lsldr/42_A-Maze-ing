from mazegen.cell import Wall
from mazegen.generator.maze_generator import MazeGenerator
from mazegen.maze import Maze
from mazegen.util import Point
from random import Random


class DFSGen(MazeGenerator):
    """Maze generator using Randomized Depth-First Search (DFS) algorithm.

    Attributes:
        maze (Maze): Maze object to be worked on.
    """

    def __init__(
            self, maze: Maze,
            perfect: bool = True,
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
        self._stack: list[Point] = []
        # Pre-populate visited with 42 pattern cells so DFS ignores them
        self._visited: set[Point] = set(self.maze.pattern_cells)

    def next(self) -> tuple[Maze, Point | None, list[Point] | None]:
        """Generate next step in maze generation.

        Returns:
            tuple[Maze, Point | None, list[Point] | None]: A tuple containing:
                - Maze: The modified maze instance.
                - Point | None: Optional coordinate of the last checked cell.
                - list[Point] | None: Optional stack of active search path.
        """
        # 1. Initialize DFS from random point
        if not self._stack and self.maze.entry not in self._visited:
            randx = self._rand.randrange(self.maze.size.x)
            randy = self._rand.randrange(self.maze.size.y)
            pos = Point(randx, randy)
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
            # Backtrack from a dead end, then
            # look for the prev cell's neighbors until the maze is ready
            self._stack.pop()
            return (self.maze, pos, self._stack.copy())

    def finish(self) -> Maze:
        """Run generation to completion.

        Returns:
            Maze: The fully generated maze object.
        """
        while not self.maze.is_ready() and (
            self._stack or self.maze.entry not in self._visited
        ):
            self.next()

        # If PERFECT is False, apply braiding
        if not self._perfect:
            self._braid_maze()

        return self.maze
