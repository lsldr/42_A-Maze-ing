# A-Maze-ing

A maze game and library project built around the `mazegen` package. The project combines generation algorithms, pathfinding, and a graphical maze application for experimentation and gameplay.

## Project layout

- `a_maze_ing.py` — main graphical app entry point
- `config.txt` — default runtime configuration
- `input_parser.py` — config parsing for the app
- `gui/` — UI and rendering code
- `mazegen/` — the reusable maze-generation and pathfinding library
- `test_scripts/` — root-level verification helpers and analyzer scripts
- `lib/` — local dependency wheel(s), including `mlx`

## What `mazegen` does

`mazegen` provides a small toolkit for building mazes and solving them:

- Maze generators:
  - `DFSGen` (randomized depth-first search)
  - `WilsonsGen` (Wilson's algorithm)
  - `IRK_Gen` (iterative randomized Kruskal)
- Pathfinders:
  - `BFSPathfinder` (guaranteed shortest path in unit-cost mazes)
  - `AStarPathfinder` (heuristic shortest-path search)
- Maze model primitives:
  - `Maze`
  - `Cell`
  - `Wall`
  - `Point`

The library represents each maze cell with walls, opens passages between neighbours, and can either generate a perfect maze or a more open, braided maze depending on the generator configuration.

## Quick start for the library

From the project root:

```bash
cd /home/aman/42/A-Maze-ing
uv sync
```

Then use the library in Python:

```python
from random import Random
from mazegen import DFSGen, BFSPathfinder, Maze, Point

maze = Maze(Point(10, 10), Point(0, 0), Point(9, 9))
gen = DFSGen(maze=maze, rand=Random(42), perfect=True)
gen.finish()

pathfinder = BFSPathfinder(maze)
path = pathfinder.finish()
print(path)
```

## Wheel installation

To build the `mazegen` package into a wheel:

```bash
cd /home/aman/42/A-Maze-ing/mazegen
uv build
```

This creates a wheel in `mazegen/dist/`.

To install it elsewhere:

```bash
pip install /home/aman/42/A-Maze-ing/mazegen/dist/mazegen-*.whl
```

Or, if you want to install it into the current environment from the built wheel:

```bash
python -m pip install --force-reinstall ./mazegen/dist/mazegen-*.whl
```

After installation, the package can be imported as:

```python
from mazegen import DFSGen, Maze, Point, BFSPathfinder
```

## Root-level testing helpers

The root `test_scripts/` directory contains helper utilities for sanity-checking generated mazes.

### `test_scripts/diff_case_tester.py`

This script generates mazes for a few dimensions and runs the analyzer against each result.

```bash
cd /home/aman/42/A-Maze-ing
uv run python test_scripts/diff_case_tester.py DFSGen
uv run python test_scripts/diff_case_tester.py WilsonsGen
uv run python test_scripts/diff_case_tester.py IRK_Gen
```

### `test_scripts/maze_analyzer.py`

This analyzer inspects a maze text export and checks things like:

- wall coherence between adjacent cells
- connectivity and region size
- loop count
- dead-end count
- malformed input detection

## How the algorithms work, briefly

### Generation

- `DFSGen` performs randomized depth-first traversal with a stack. It carves passages while backtracking, producing classic tree-like mazes.
- `WilsonsGen` uses loop-erased random walks, which tends to create more uniform maze patterns.
- `IRK_Gen` uses a disjoint-set structure to add passages only when they connect separate regions, producing a valid spanning tree efficiently.

### Pathfinding

- `BFSPathfinder` explores cells level by level, which guarantees the shortest route in unit-cost mazes.
- `AStarPathfinder` uses a heuristic based on Manhattan distance to focus the search toward the exit while still finding an optimal path.

## Running the app

```bash
cd /home/aman/42/A-Maze-ing
uv run a_maze_ing.py config.txt
```

## Linting commands

From the project root:

```bash
flake8 . --exclude=.venv --cache-dir=/tmp/flake8-cache
mypy . --exclude '(^\.venv$|^\.git$|^__pycache__$)' --cache-dir=/tmp/mypy-cache
```

These commands check the project without writing cache files into the repository.

## Notes

- The root project depends on the local `mazegen` workspace package via `uv`.
- The `mazegen` subproject is itself configured as a separate Python package with its own `pytest` setup and tests under `mazegen/tests/`.
