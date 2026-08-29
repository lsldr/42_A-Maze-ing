from __future__ import annotations

from abc import ABC, abstractmethod
from mazegen.util import Point
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mazegen.maze import Maze


class Pathfinder(ABC):
    """Base class for maze pathfinding algorithms.

    Attributes:
        maze (Maze): Maze instance where pathfinding is performed.
    """

    def __init__(self, maze: Maze) -> None:
        """Initialize the pathfinder.

        Args:
            maze (Maze): Maze where path is to be found.
        """
        self.maze = maze
        self._done = False
        self._path: list[Point] = []

    def is_done(self) -> bool:
        """Check if pathfinding has finished.

        Returns:
            bool: True if path was found or search exhausted, False otherwise.
        """
        return self._done

    def get_path(self) -> list[Point]:
        """Get the calculated path.

        Returns:
            list[Point]: Shortest path from start to end, or empty
                if not ready.
        """
        return self._path

    @abstractmethod
    def next(self) -> tuple[bool, list[Point]]:
        """Generate next step in pathfinding.

        Returns:
            tuple[bool, list[Point]]: A tuple containing:
                - bool: True if pathfinding finished, False otherwise.
                - list[Point]: Explored coordinates for visualization.
        """

    def finish(self) -> list[Point]:
        """Run pathfinding to completion.

        Returns:
            list[Point]: Shortest path from entry to exit.
        """
        while not self.is_done():
            self.next()
        return self._path
