from abc import ABC, abstractmethod
from mazegen.maze import Maze


class Pathfinder(ABC):
    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    @abstractmethod
    def is_ready(self) -> bool:
        """Check if path was found

        Returns:
            True if path was found, False otherwise
        """

    @abstractmethod
    def get_path(self) -> list[tuple[int, int]] | None:
        """Returns shortest path from start to end
        or None if path is not ready"""

    @abstractmethod
    def next(self) -> list[tuple[int, int]]:
        """Generate next step in pathfinding

        Returns:
            list of checked spaces
        """

    @abstractmethod
    def finish(self) -> list[tuple[int, int]]:
        """Finish maze generation and return finished path

        Returns:
            shortest path
        """
