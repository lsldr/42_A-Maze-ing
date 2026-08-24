import random
from enum import IntFlag


class Wall(IntFlag):
    """Bitmask representation for grid cell walls."""

    NORTH = 1  # Bit 0 (1 << 0)
    EAST = 2  # Bit 1 (1 << 1)
    SOUTH = 4  # Bit 2 (1 << 2)
    WEST = 8  # Bit 3 (1 << 3)


DIRECTIONS: list[tuple[int, int, Wall, Wall]] = [
    (0, -1, Wall.NORTH, Wall.SOUTH),  # Move North
    (1, 0, Wall.EAST, Wall.WEST),  # Move East
    (0, 1, Wall.SOUTH, Wall.NORTH),  # Move South
    (-1, 0, Wall.WEST, Wall.EAST),  # Move West
]


def get_unvisited_neighbors(
    cx: int,
    cy: int,
    width: int,
    height: int,
    visited: set[tuple[int, int]],
    pattern_42: set[tuple[int, int]],
) -> list[tuple[int, int, Wall, Wall]]:
    """Returns valid, unvisited neighbor coordinates and wall masks."""

    neighbors = []
    for dx, dy, c_wall, n_wall in DIRECTIONS:
        nx, ny = cx + dx, cy + dy

        # Check for boundaries, visited cells, and immutable (pattern) cells
        if 0 <= nx < width and 0 <= ny < height:
            if (nx, ny) not in visited and (nx, ny) not in pattern_42:
                neighbors.append(nx, ny, c_wall, n_wall)

    return neighbors


def add_loops(
    grid: list[list[int]],
    width: int,
    height: int,
    pattern_42: set,
    loop_factor: float = 0.05,
):
    """Randomly knocks down a small percentage of
    the remaining walls to create multiple paths."""
    extra_walls_to_remove = int(width * height * loop_factor)
    for _ in range(extra_walls_to_remove):
        rx, ry = random.randint(0, width - 1), random.randint(0, height - 1)
        if (rx, ry) in pattern_42:
            continue
        # Pick a random neighbor and remove the wall between them
        dx, dy, c_wall, n_wall = random.choice(DIRECTIONS)
        nx, ny = rx + dx, ry + dy
        if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in pattern_42:
            grid[ry][rx] &= ~c_wall
            grid[ny][nx] &= ~n_wall


def dfs_maze_gen(configs: dict) -> list[list[int]]:
    width = configs["width"]
    height = configs["height"]
    entry = configs["entry"]
    pattern_42 = configs.get("pattern_cells", set())
    perfect = configs.get("perfect", True)

    # 1. Initialize all cells with 15 (all 4 walls intact)
    grid = [[15 for _ in range(width)] for _ in range(height)]

    # 2. Start DFS from Entry
    start_x, start_y = entry
    stack = [(start_x, start_y)]
    visited = {(start_x, start_y)}

    while stack:
        cx, cy = stack[-1]
        neighbors = get_unvisited_neighbors(
            cx, cy, width, height, visited, pattern_42
        )

        if neighbors:
            # Choose a random neighbor and carve a passage
            nx, ny, c_wall, n_wall = random.choice(neighbors)

            grid[cy][cx] &= ~c_wall
            grid[ny][nx] &= ~n_wall

            visited.add((nx, ny))
            stack.append((nx, ny))
        else:
            # Backtrack when at a dead end
            stack.pop()

    # 3. If PERFECT is False, randomly remove a few extra walls to create loops
    if not perfect:
        add_loops(grid, width, height, pattern_42)

    return grid
