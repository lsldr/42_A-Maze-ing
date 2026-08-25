from mazegen.cell import Wall
from mazegen.generator.maze_generator import Maze_Generator
from mazegen.maze import Maze
from mazegen.util import Point
from random import Random


class DFS_gen(Maze_Generator):
    def __init__(self, maze: Maze, rand: Random, perfect: bool = True) -> None:
        super().__init__(maze, rand, perfect)
        self._stack: list[Point] = []
        # Pre-populate visited with pattern cells so DFS ignores them
        self._visited: set[Point] = set(self.maze.pattern_cells)

    def next(self) -> tuple[Maze, Point | None, list[Point] | None]:
        # 1. Initialize DFS from Entry
        if not self._stack and self.maze.entry not in self._visited:
            pos = self.maze.entry
            self._visited.add(pos)
            self.maze.get_cell(pos).visited = True
            self._stack.append(pos)
            return (self.maze, pos, self._stack.copy())

        # Generation complete or stack emptied
        if not self._stack:
            return (self.maze, None, [])

        pos = self._stack[-1]
        x, y = pos

        # 2. Find valid, unvisited, non-pattern neighbors
        neighbors: list[tuple[Wall, Point]] = []
        for side in [Wall.NORTH, Wall.EAST, Wall.SOUTH, Wall.WEST]:
            dx, dy = side.get_direction()
            npos = Point(x + dx, y + dy)
            if self.maze.in_bounds(npos) and npos not in self._visited:
                neighbors.append((side, npos))

        if neighbors:
            # Pick a random neighbor and carve a wall
            side, npos = self._rand.choice(neighbors)
            if self.maze.try_open_wall(pos, side):
                self._visited.add(npos)
                self.maze.get_cell(npos).visited = True
                self._stack.append(npos)
            return (self.maze, npos, self._stack.copy())
        else:
            # Backtrack from a dead end
            # Then loook for the prev cell's neighbors if it's in stack
            self._stack.pop()
            return (self.maze, pos, self._stack.copy())

    def _braid_maze(self) -> None:
        """Eliminates dead ends while preventing 3x3 open areas
        and respecting 42 pattern."""
        all_directions = [Wall.NORTH, Wall.EAST, Wall.SOUTH, Wall.WEST]

        while True:
            # 1. Collect all dead ends (degree == 1)
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

            for pos in dead_ends:
                if self.maze.count_open_passages(pos) != 1:
                    continue  # Already resolved in this pass

                dead_end_candidates: list[tuple[Wall, Point]] = []
                regular_candidates: list[tuple[Wall, Point]] = []

                for side in all_directions:
                    # Wall must be currently closed
                    if side not in self.maze.get_cell(pos).walls:
                        continue

                    dx, dy = side.get_direction()
                    npos = Point(pos.x + dx, pos.y + dy)

                    if (
                        not self.maze.in_bounds(npos)
                        or self.maze.get_cell(npos).lock
                    ):
                        continue

                    # Reject if it would create a 3x3 open room
                    if self.maze.would_create_3x3_room(pos, side):
                        continue

                    if self.maze.count_open_passages(npos) == 1:
                        dead_end_candidates.append((side, npos))
                    else:
                        regular_candidates.append((side, npos))

                # Priority 1: Connect to another dead end
                # Priority 2: Connect to an adjacent corridor
                chosen_pool = dead_end_candidates or regular_candidates
                if chosen_pool:
                    side, _ = self._rand.choice(chosen_pool)
                    self.maze.try_open_wall(pos, side)
                    modified_any = True

            # If no dead ends could be safely removed in a full pass, stop
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
                    ):
                        if not self.maze.would_create_3x3_room(pos, side):
                            candidates.append(side)
                if not candidates:
                    break
                side = self._rand.choice(candidates)
                self.maze.try_open_wall(pos, side)

    def finish(self) -> Maze:
        """Run generation to completion."""
        while not self.maze.is_ready() and (
            self._stack or self.maze.entry not in self._visited
        ):
            self.next()

        # If PERFECT is False, apply braiding
        if not self._perfect:
            self._braid_maze()

        return self.maze
