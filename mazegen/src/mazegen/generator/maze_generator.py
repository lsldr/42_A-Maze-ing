from abc import ABC, abstractmethod
from mazegen import Wall
from mazegen.maze import Maze
from mazegen.util import Point
from random import Random


class MazeGenerator(ABC):
    """Abstract base class for maze generators.

    Attributes:
        maze (Maze): Maze instance being generated.
    """

    def __init__(
        self, maze: Maze, rand: Random, perfect: bool = False
    ) -> None:
        """Initialize generator.

        Args:
            maze (Maze): Object to be worked on.
            rand (Random): Random number generator.
            perfect (bool): Defines if maze should have only
                one solution (True) or more (False).
        """
        self._rand = rand
        self.maze = maze
        self._perfect = perfect

    def is_ready(self) -> bool:
        """Check if maze generation is complete.

        Returns:
            bool: True if maze is fully generated, False otherwise.

        Raises:
            MazeError: If maze is malformed.
        """
        return self.maze.is_ready()

    @abstractmethod
    def next(self) -> tuple[Maze, Point | None, list[Point] | None]:
        """Generate next step in maze generation.

        Returns:
            tuple[Maze, Point | None, list[Point] | None]: A tuple containing:
                - Maze: The modified maze instance.
                - Point | None: Optional coordinate of the last checked cell.
                - list[Point] | None: Optional stack of positions.
        """
        ...

    def _braid_maze(self) -> None:
        """Eliminates dead ends while preventing 3x3 open areas
        and respecting 42 pattern."""
        all_directions = [Wall.NORTH, Wall.EAST, Wall.SOUTH, Wall.WEST]

        # Max retry passes to ensure all dead ends are resolved
        max_passes = 10
        for _ in range(max_passes):
            # 1. Collect all current dead ends
            dead_ends: list[Point] = [
                Point(x, y)
                for x in range(self.maze.size.x)
                for y in range(self.maze.size.y)
                if not self.maze.get_cell(Point(x, y)).lock
                and self.maze.count_open_passages(Point(x, y)) == 1
            ]
            if not dead_ends:
                break

            self._rand.shuffle(dead_ends)
            modified_any = False

            # --- PHASE 1: Try to pair Dead Ends together first ---
            for pos in dead_ends:
                if self.maze.count_open_passages(pos) != 1:
                    continue  # Already resolved

                dead_end_candidates: list[tuple[Wall, Point]] = []
                for side in all_directions:
                    if side not in self.maze.get_cell(pos).walls:
                        continue
                    dx, dy = side.get_direction()
                    npos = Point(pos.x + dx, pos.y + dy)

                    if (
                        self.maze.in_bounds(npos)
                        and not self.maze.get_cell(npos).lock
                        and not self.maze.would_create_3x3_room(pos, side)
                        and self.maze.count_open_passages(npos) == 1
                    ):
                        dead_end_candidates.append((side, npos))

                if dead_end_candidates:
                    side, _ = self._rand.choice(dead_end_candidates)
                    self.maze.try_open_wall(pos, side)
                    modified_any = True

            # --- PHASE 2: Connect remaining Dead Ends to regular corridors ---
            for pos in dead_ends:
                if self.maze.count_open_passages(pos) != 1:
                    continue  # Resolved in Phase 1

                regular_candidates: list[tuple[Wall, Point]] = []
                for side in all_directions:
                    if side not in self.maze.get_cell(pos).walls:
                        continue
                    dx, dy = side.get_direction()
                    npos = Point(pos.x + dx, pos.y + dy)

                    if (
                        self.maze.in_bounds(npos)
                        and not self.maze.get_cell(npos).lock
                        and not self.maze.would_create_3x3_room(pos, side)
                    ):
                        regular_candidates.append((side, npos))

                if regular_candidates:
                    # Sort/prefer neighbors with fewest open passages
                    #  to avoid dense hubs
                    regular_candidates.sort(
                        key=lambda item: self.maze.count_open_passages(item[1])
                    )
                    # Pick randomly among candidates with
                    # the lowest passage count
                    min_deg = self.maze.count_open_passages(
                        regular_candidates[0][1]
                    )
                    best_candidates = [
                        c
                        for c in regular_candidates
                        if self.maze.count_open_passages(c[1]) == min_deg
                    ]
                    side, _ = self._rand.choice(best_candidates)
                    self.maze.try_open_wall(pos, side)
                    modified_any = True

            # If no modifications could be safely made in an entire pass, break
            if not modified_any:
                break

        # 2. Ensure corners and centre have at least 2 open passages
        self._ensure_special_cells_open()

    def _ensure_special_cells_open(self) -> None:
        """Guarantees that the 4 corners and centre have degree >= 2."""
        special_cells = [
            Point(0, 0),
            Point(self.maze.size.x - 1, 0),
            Point(0, self.maze.size.y - 1),
            Point(self.maze.size.x - 1, self.maze.size.y - 1),
            Point(self.maze.size.x // 2, self.maze.size.y // 2),
        ]
        all_directions = [Wall.NORTH, Wall.EAST, Wall.SOUTH, Wall.WEST]

        for pos in special_cells:
            if not self.maze.in_bounds(pos) or self.maze.get_cell(pos).lock:
                continue
            while self.maze.count_open_passages(pos) < 2:
                candidates = []
                for side in all_directions:
                    if side not in self.maze.get_cell(pos).walls:
                        continue
                    dx, dy = side.get_direction()
                    npos = Point(pos.x + dx, pos.y + dy)
                    if (
                        self.maze.in_bounds(npos)
                        and not self.maze.get_cell(npos).lock
                    ) and not self.maze.would_create_3x3_room(pos, side):
                        candidates.append(side)
                if not candidates:
                    break
                side = self._rand.choice(candidates)
                self.maze.try_open_wall(pos, side)

    def finish(self) -> Maze:
        """Run generation to completion.

        Returns:
            Maze: The fully generated maze object.
        """
        while not self.maze.is_ready():
            self.next()

        if not self._perfect:
            self._braid_maze()
        return self.maze
