from PIL.WalImageFile import WalImageFile
from abc import ABC, abstractmethod
from mazegen.maze import Maze
from random import Random


class Maze_Generator(ABC):
    def __init__(self,
                 maze: Maze, rand: Random, perfect: bool = False) -> None:
        self._rand = rand
        self.maze = maze
        self._perfect = perfect

    def is_ready(self) -> bool:
        """Check if maze is ready, locked cells are ignored

        Returns:
            True if maze if fully generated, False otherwise

        Raises:
            MazeError if maze is malformed
        """
        return self.maze.is_ready()

    @abstractmethod
    def next(self) -> tuple[Maze,
                            tuple[int, int] | None,
                            list[tuple[int, int]] | None]:
        """Generate next step in maze generation

        Returns:
            Maze: maze that was modified
            (x, y): optional position of the last checked cell
            optional stack of positions
        """

    def finish(self) -> Maze:
        """Finish maze generation and return finished maze

        Returns:
            ready maze
        """
        maze = self.maze
        while not self.maze.is_ready():
            maze, _, _ = self.next()
        return maze
