from mazegen.maze import Maze
from mazegen.pathfinder.pathfinder import Pathfinder
from mazegen.util import Point


class BFS_pathfinder(Pathfinder):
    def __init__(self, maze: Maze) -> None:
        super().__init__(maze)
        self._stack: list[Point] = []

    def next(self) -> tuple[bool, list[Point]]:
        if self._done:
            return True, self._stack.copy()
        if not self._stack:
            self._stack.append(self.maze.entry)
            if self.maze.entry == self.maze.exit:
                self._done = True
                self._path.append(self.maze.entry)
            return self._done, self._stack.copy()
        return False, self._stack
