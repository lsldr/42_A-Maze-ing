from __future__ import annotations

from collections import deque
from mazegen.cell import Wall
from mazegen.pathfinder.pathfinder import Pathfinder
from mazegen.util import Point
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mazegen.maze import Maze


class BFSPathfinder(Pathfinder):
    def __init__(self, maze: Maze) -> None:
        super().__init__(maze)
        self._queue: deque[Point] = deque([self.maze.entry])
        self._visited: set[Point] = {self.maze.entry}
        self._parent: dict[Point, Point] = {}
        self._explored: list[Point] = [self.maze.entry]

    def _reconstruct_path(self) -> list[Point]:
        """Traces from exit point to entry using the parent dictionary

        Returns the list of points for the entry-to-exit path"""

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
        """After popping (with deque.popleft()) it from the queue, looks
        at the current cell's neighbors that are reachable, then adds them
        all to the queue (deque list), visited (set), parent(dict to backtrack)
        and explored (list for visualization purposes). In each call,
        continues to do this for current cells, gradually looking for
        closes neighbor cells first and continuing. Over time, the explored
        branches that did not lead to exit are all out of queue.
        Whenever the current reaches exit, this means that the shortest path
        to exit from entry is reached (since shortest ways are explored first),
        so the backtracking method is called to build the path (list[Point])
        to be returned from the class.


        Returns a tuple with a bool indicating if the path was found
        and a list explored paths in order of exploration. Walls are
        searched starting from the North and clockwise as of the current
        version."""

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
