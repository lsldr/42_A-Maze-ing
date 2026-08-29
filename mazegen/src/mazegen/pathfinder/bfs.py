from __future__ import annotations

from collections import deque
from mazegen.cell import Wall
from mazegen.pathfinder.pathfinder import Pathfinder
from mazegen.util import Point
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mazegen.maze import Maze


class BFSPathfinder(Pathfinder):
    """Find path in maze using Breadth-First Search (BFS) algorithm.

    Attributes:
        maze (Maze): The maze instance being solved.
    """

    def __init__(self, maze: Maze) -> None:
        """Initialize the BFS pathfinder.

        Args:
            maze (Maze): Maze where the path is to be found.
        """
        super().__init__(maze)
        self._queue: deque[Point] = deque([self.maze.entry])
        self._visited: set[Point] = {self.maze.entry}
        self._parent: dict[Point, Point] = {}
        self._explored: list[Point] = [self.maze.entry]

    def _reconstruct_path(self) -> list[Point]:
        """Trace from exit point to entry using the parent dictionary.

        Returns:
            list[Point]: Ordered list of points forming the entry-to-exit path.
        """
        path: list[Point] = []
        c_point: Point | None = self.maze.exit
        while c_point is not None and c_point != self.maze.entry:
            path.append(c_point)
            c_point = self._parent.get(c_point)

        path.append(self.maze.entry)
        path.reverse()
        self.maze.path = path
        return path

    def next(self) -> tuple[bool, list[Point]]:
        """Generate next step in BFS pathfinding.

        Returns:
            tuple[bool, list[Point]]: A tuple containing:
                - bool: True if exit was reached or queue is exhausted.
                - list[Point]: Explored points for GUI visualization.
        """

        all_sides = [Wall.NORTH, Wall.EAST, Wall.SOUTH, Wall.WEST]
        if self._done or not self._queue:
            self._done = True
            return True, self._explored

        current = self._queue.popleft()

        # If exit reached
        if current == self.maze.exit:
            self._path = self._reconstruct_path()
            self._done = True
            return True, self._explored

        c_cell = self.maze.get_cell(current)
        for side in all_sides:
            if side not in c_cell.walls:
                dx, dy = side.get_direction()
                npos = Point(current.x + dx, current.y + dy)

                if self.maze.in_bounds(npos) and npos not in self._visited:
                    self._visited.add(npos)
                    self._parent[npos] = current
                    self._queue.append(npos)
                    self._explored.append(npos)
        if not self._queue:
            self._done = True
            return True, self._explored
        return False, self._explored
