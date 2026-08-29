from __future__ import annotations

import heapq
from mazegen.cell import Wall
from mazegen.pathfinder.pathfinder import Pathfinder
from mazegen.util import Point
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mazegen.maze import Maze


class AStarPathfinder(Pathfinder):
    """Find path in maze using A* (A-Star) search algorithm.

    Uses Manhattan distance heuristic to guide exploration towards the exit.
    """

    def __init__(self, maze: Maze) -> None:
        """Initialize the A* pathfinder.

        Args:
            maze (Maze): The maze on which to find the path.
        """
        super().__init__(maze)
        self._counter: int = 0
        start = self.maze.entry
        h_start = self._heuristic(start)
        # Heap elements: (f_score, counter, point)
        self._open_heap: list[tuple[int, int, Point]] = [
            (h_start, self._counter, start)
        ]
        self._open_set: set[Point] = {start}
        self._closed_set: set[Point] = set()
        self._g_score: dict[Point, int] = {start: 0}
        self._parent: dict[Point, Point] = {}
        self._explored: list[Point] = [start]

    def _heuristic(self, point: Point) -> int:
        """Calculate Manhattan distance heuristic from point to exit.

        Args:
            point (Point): Current cell coordinate.

        Returns:
            int: Manhattan distance between point and maze exit.
        """
        return abs(point.x - self.maze.exit.x) + abs(point.y - self.maze.exit.y)

    def _reconstruct_path(self) -> list[Point]:
        """Trace from exit point to entry using the parent dictionary.

        Returns:
            list[Point]: Ordered list of points forming the path.
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
        """Perform next step in A* pathfinding.

        Pops the node with lowest f-score from the priority queue and explores
        its accessible cardinal neighbors.

        Returns:
            tuple[bool, list[Point]]:
                - bool: True if exit was reached or queue is exhausted.
                - list[Point]: Explored points for GUI visualization.
        """
        all_sides = [Wall.NORTH, Wall.EAST, Wall.SOUTH, Wall.WEST]
        if self._done or not self._open_heap:
            self._done = True
            return True, self._explored

        _, _, current = heapq.heappop(self._open_heap)
        self._open_set.discard(current)
        self._closed_set.add(current)

        if current == self.maze.exit:
            self._path = self._reconstruct_path()
            self._done = True
            return True, self._explored

        c_cell = self.maze.get_cell(current)
        current_g = self._g_score[current]

        for side in all_sides:
            if side not in c_cell.walls:
                dx, dy = side.get_direction()
                npos = Point(current.x + dx, current.y + dy)

                if not self.maze.in_bounds(npos) or npos in self._closed_set:
                    continue

                tentative_g = current_g + 1
                if tentative_g < self._g_score.get(npos, float("inf")):
                    self._parent[npos] = current
                    self._g_score[npos] = tentative_g
                    f_score = tentative_g + self._heuristic(npos)
                    self._counter += 1
                    heapq.heappush(
                        self._open_heap, (f_score, self._counter, npos)
                    )
                    self._open_set.add(npos)
                    if npos not in self._explored:
                        self._explored.append(npos)

        if not self._open_heap:
            self._done = True
            return True, self._explored

        return False, self._explored
