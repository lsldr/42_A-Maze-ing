from abc import ABC, abstractmethod
from mazegen.maze import Maze
from mazegen.util import Point
from collections import deque


class Pathfinder(ABC):
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self._done = False
        self._queue: list[Point] = deque([self.maze.entry])
        self._visited: set[Point] = {self.maze.entry}
        self._parent: dict[Point, Point] = dict()
        self._explored: list[Point] = [self.maze.entry]  # For UI visuals
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

    @property
    def queue(self) -> list[Point]:
        """Returns the queue of cells to explore next"""
        return self._queue

    @property
    def explored(self) -> list[Point]:
        """Returns the list of explored cells"""
        return self._explored

    @property
    def visited(self) -> set[Point]:
        """Returns the set of visited cells"""
        return self._visited

    @property
    def parent(self) -> dict[Point, Point]:
        """Returns the parent dictionary of cells"""
        return self._parent

    @abstractmethod
    def next(self) -> tuple[bool, list[Point]]:
        """Generate next step in pathfinding

        Returns:
            bool if a path was found
            list of checked spaces
        """

        if self.is_done() or not self._queue:
            return (True, self._explored)

        current = self._queue.popleft()
        self._explored.append(current)

        if current == self.maze.exit:
            while current != self.maze.entry:
                current = self._parent["current"]
            self._path = self._explored.reverse()
            self._done = True
            return (True, self._explored)

        return (False, self._explored)

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
