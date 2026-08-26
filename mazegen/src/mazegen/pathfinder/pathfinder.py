from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from mazegen.util import Point

if TYPE_CHECKING:
    from mazegen.maze import Maze


class Pathfinder(ABC):
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self._done = False
        self._path: list[Point] = []

    def is_done(self) -> bool:
        """Check if path was found."""
        return self._done

    def get_path(self) -> list[Point]:
        """Returns shortest path from start to end, or empty if not ready."""
        return self._path

    @abstractmethod
    def next(self) -> tuple[bool, list[Point]]:
        """Generate next step in pathfinding.

        Returns:
            bool: True if pathfinding finished, False otherwise.
            list[Point]: List of explored/checked spaces for visualization.
        """
        pass

    def finish(self) -> list[Point]:
        """Run pathfinding to completion and return the path."""
        while not self.is_done():
            self.next()
        return self._path
