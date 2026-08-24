from abc import ABC, abstractmethod
from mazegen.maze import Maze
from mazegen.util import Point


class Pathfinder(ABC):
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self._done = False
        self._path: list[Point] = []

    def is_done(self) -> bool:
        """Check if path was found

        Returns:
            True if path was found, False otherwise
        """
        return self._done

    def get_path(self) -> list[Point]:
        """Returns shortest path from start to end
        or empty if path is not ready"""
        return self._path

    @abstractmethod
    def next(self) -> tuple[bool, list[Point]]:
        """Generate next step in pathfinding

        Returns:
            bool is path found
            list of checked spaces
        """

    @abstractmethod
    def finish(self) -> list[Point]:
        """Finish maze generation and return finished path

        Returns:
            shortest path
        """
        done, _ = self.next()
        while not done:
            done, _ = self.next()
        return self._path
