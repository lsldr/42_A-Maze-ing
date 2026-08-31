*This project has been created as part of the 42 curriculum by asuleime, msowinsk.*

# A-Maze-ing

## Description

A-Maze-ing is a maze-generation and pathfinding project built around a reusable Python library called `mazegen` and a graphical application entry point in the root folder. The goal of the project is to generate mazes, manage their structure, solve them with different search strategies, and present the result in an interactive graphical interface.

The project combines a library component and an application layer:
- `mazegen/` contains the reusable maze engine with generation algorithms and pathfinders.
- `a_maze_ing.py` is the root entry point that loads configuration and runs the graphical app.
- `gui/` handles the display and interaction layer.
- `config.txt` stores the default runtime configuration.

The program can generate mazes using different algorithms, then solve them with BFS or A* and optionally render them in a graphical window. The library code is intentionally separated from the application layer to make it reusable in other programs and tests.

## Instructions

### Prerequisites

- Python 3.13 or later
- `uv` for dependency and workspace management
- local `mlx` wheel stored in `lib/`

### Installation and setup

From the project root:

```bash
cd /home/aman/42/A-Maze-ing
uv sync
```

This installs the workspace dependencies and makes the local `mazegen` package available to the application environment.

### Run the application

```bash
cd /home/aman/42/A-Maze-ing
uv run a_maze_ing.py config.txt
```

### Build and install the library wheel

```bash
cd /home/aman/42/A-Maze-ing/mazegen
uv build
python -m pip install --force-reinstall ./dist/mazegen-*.whl
```

After installation, the package can be used as:

```python
from mazegen import DFSGen, BFSPathfinder, Maze, Point
```

### Run tests quickly

```bash
cd /home/aman/42/A-Maze-ing
make pytest-fast
```

For more detail, use:

```bash
make pytest-verbose
```

### Linting

```bash
cd /home/aman/42/A-Maze-ing
make lint
```

## Configuration file structure

The root configuration file format is defined in `config.txt` and parsed by `input_parser.py`.

```ini
# required by project file (these are mandatory)
WIDTH=10
HEIGHT=10
ENTRY=1,1
EXIT=9,9
OUTPUT_FILE=maze.txt
PERFECT=False

# seed for maze generation, can be int, none or omitted
SEED=42

# algorithm for maze generation
# available: dfs, wilson, irk
# default: dfs
MAZEGEN=wilson

# pathfinding algorithm
# available: bfs, astar
# default: bfs
# PATHFINDING=astar
```

### Field descriptions

- `WIDTH` and `HEIGHT`: grid dimensions
- `ENTRY` and `EXIT`: start and end coordinates in `x,y` form
- `OUTPUT_FILE`: destination file path for exported maze output
- `PERFECT`: if set to `True`, the maze has a single valid solution; if `False`, it may be braided
- `SEED`: reproducible random generation seed
- `MAZEGEN`: selected generation algorithm
- `PATHFINDING`: selected solver

## Chosen algorithm

The project supports multiple generation algorithms, including:
- `DFSGen` — randomized depth-first search
- `WilsonsGen` — loop-erased random walk
- `IRK_Gen` — iterative randomized Kruskal

The default strategy used in the project is a randomized depth-first approach, because it is simple, fast, and produces reliable maze structures with a clear spanning-tree logic. It is also very easy to test and reason about, which makes the code reusable and stable.

Wilson's algorithm was chosen because of how uniform the maze patterns appear as a result of different tries. This improves reproducibility.

Kruskal's algorithm was used due to its speed and use of basic set theory concepts (once all cells are connected with random choice of walls, they become a single set in a disjoint-set).

## Why this algorithm

Depth-first generation was chosen as the main default because it offers:
- efficient runtime complexity on typical grid sizes
- deterministic behavior when seeded
- easy-to-verify maze connectivity
- a simple implementation that fits the library API well

The library still exposes the other algorithms so the project can compare generation behaviors and demonstrate algorithmic diversity.

## Reusable code

The reusable part of the project is concentrated in the `mazegen` package:
- `Maze` stores the grid, bounds, entry, exit, and path information
- `Cell` represents each cell and manages wall state and locking behavior
- `Point` provides a lightweight coordinate object used everywhere in the grid
- `DFSGen`, `WilsonsGen`, and `IRK_Gen` share the same `MazeGenerator` interface
- `BFSPathfinder` and `AStarPathfinder` share the `Pathfinder` interface

This makes the generation and solving logic modular and reusable in tests, scripts, or future graphical or CLI tools without duplicating the maze logic.

## Project management and team organization

### Roles

- Aman (asuleime) — input parsing, core maze structure and attributes (partial), DFS algorithm (partial) and Kruskal's algorithm for maze generation, BFS and A* pathfinding algorithms, GUI (partial), root directory and `mazegen` package testing scripts
- Mateusz (msowinsk) — uv packaging and module structure, OOP logic (inheritance, abstract methods) of the maze generator and pathfinder algorithms, documentation, GUI (partial, including the MLX part), DFS algorithm (partial) and Wilson's algorithm for maze generation

### Modularity

The project has a modular architecture, with the `mazegen` package taking responsibility for all reusable logic. This separation improved clarity and made it easier to test pathfinding and generation independently from the GUI.

### What worked well

- Clear separation between domain logic and display logic
- Reusable `mazegen` structures made testing easier
- A single configuration file simplified runtime setup
- Multiple maze generators made algorithm comparisons straightforward

### What could be added

- Starter GUI that would prompt the user to add configs
- More elaborate documentation of the configuration defaults and supported commands

### Tools used

- `uv` — workspace and dependency management
- `pytest` — automated validation of the library
- `flake8` — style checks
- `mypy` — static type checking
- `MiniLibX` and `Pillow` — graphical rendering support
- `Git` / version control — project coordination

## Advanced features implemented

The project includes several features beyond a simple single-algorithm prototype:
- multiple generation strategies: DFS, Wilson's, and IRK
- multiple pathfinding strategies: BFS and A* 
- no dead-end mazes for `PERFECT=False`
- pattern-cell handling for fixed blocked regions
- configurable runtime setup from `config.txt`
- root-level diagnostic scripts for generated maze validation

## Resources

### Classic references

- The Art of Computer Programming, volume 4, relevant sections on graph algorithms and randomized generation
- Introduction to Algorithms by Cormen, Leiserson, Rivest, and Stein
- Maze generation algorithms: depth-first search, Wilson's algorithm, and Kruskal-based approaches
- BFS and A* pathfinding references and tutorials from classic algorithm textbooks and online computer science material

### AI usage

AI was used in the project for:
- helping with explanations of type-checker issues
- checking documentation structure and README wording
- Learning about different algorithms and finding good sources

## Repository structure

```text
A-Maze-ing/
├── a_maze_ing.py
├── config.txt
├── input_parser.py
├── Makefile
├── README.md
├── lib/
├── gui/
├── mazegen/
│   ├── src/mazegen/
│   ├── tests/
│   └── pyproject.toml
├── test_scripts/
└── maze.txt
```

## Summary

A-Maze-ing is a maze project that brings together algorithmic generation, pathfinding, configuration parsing, and a graphical display layer. The reusable `mazegen` library is the heart of the project, while the root application demonstrates how it can be used in a practical interface.
