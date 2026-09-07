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

## Mazegen package documentation (from the package README.md)




## mazegen

A Python library for generating and solving mazes using multiple algorithms. mazegen provides efficient implementations of popular maze generation and pathfinding algorithms with both perfect and braided maze support.

### Features

- **Multiple Maze Generation Algorithms:**
  - Randomized Depth-First Search (DFS)
  - Wilson's Algorithm
  - Iterative Randomized Kruskal's (IRK)

- **Multiple Pathfinding Algorithms:**
  - Breadth-First Search (BFS) - guaranteed shortest path with exploration of all possible paths at each point
  - A* Search - optimized pathfinding with heuristics based on entry and exit point coordinates (provided in the configs text file)

- **Perfect and Braided Mazes:** Generate perfect mazes (single solution) or braided mazes (multiple solutions and no dead-ends)

- **Step-by-Step Execution:** Generate mazes or find paths incrementally for visualization and education

- **42 pattern:** The central rectangle region 7 cells wide and 5 cells high has a pattern with 18 cells that resemble the number "42"

- **Simple and Intuitive API**

### Installation

- *First, Ensure you downloaded the .whl or built it from the cloned repository*

```bash
pip install mazegen
```

### Quick Start

```python
from mazegen import DFSGen, BFSPathfinder, Point, Maze

# Generate a maze using Depth-First Search
maze = Maze(size=Point(20, 20), entry=Point(1, 3), exit=Point(18, 18))
generator = DFSGen(maze)
generator.finish()

# Find the shortest path through the maze
pathfinder = BFSPathfinder(maze)
path = pathfinder.finish()

print(f"Maze generated! Found path of length: {len(path)}")

# Or generate step-by-step for visualization
maze = Maze(Point(20, 20))
generator = DFSGen(maze)
while not generator.is_done():
    generator.next()  # Do one generation step
    # Update your GUI here

maze = generator.finish()
```

### Maze Generation Algorithms

#### 1. Randomized Depth-First Search (DFS)

**Overview:** DFS creates mazes by carving passages using a stack-based approach. Starting from a random cell, it explores as far as possible along each branch before backtracking, naturally creating long corridors and a tree-like structure.

**How It Works:**

1. Start at a random cell, mark as visited
2. While cells remain unvisited:
   - From current cell, find all unvisited neighbors
   - Randomly choose one neighbor
   - Carve an opening between current and neighbor
   - Move to neighbor (push to stack)
   - If no unvisited neighbors, backtrack (pop from stack)

**Characteristics:**
- **Simplicity:** Easy to understand and implement
- **Speed:** O(w × h) time complexity (linear)
- **Long Corridors:** Produces mazes with long, winding passages
- **Texture:** Creates very recognizable patterns (long branching corridors)
- **Possible Direction Bias:** May bias toward certain directions depending on neighbor selection order

**Use Cases:** Good for general purpose maze generation, fast generation, educational purposes

**Example:**
```python
from mazegen import DFSGen, Maze

# Create a 50x50 perfect maze
maze = Maze(Point(50, 50))
gen = DFSGen(maze=maze, perfect=True)
gen.finish()

# Or create a braided maze (with multiple solutions)
maze = Maze(Point(50, 50))
gen = DFSGen(maze=maze, perfect=False)
maze = gen.finish()
```

---

#### 2. Wilson's Algorithm

**Overview:** Wilson's algorithm creates mazes using loop-erased random walks. It starts with one cell and repeatedly performs random walks from unvisited cells, carving passages only when a walk connects to the existing maze. This produces uniform random spanning trees.

**How It Works:**

1. Mark one random cell as part of the maze
2. While unvisited cells remain:
   - Start a random walk from any unvisited cell
   - Walk randomly to adjacent cells
   - If walk revisits itself, erase the loop and continue from the loop point
   - When walk reaches the existing maze, carve the entire path into the maze
   - Mark all path cells as visited

**Characteristics:**
- **Uniform Distribution:** Each possible maze equally likely
- **Perfect Guarantee:** Always produces perfect mazes (single solution)
- **Balanced Texture:** Creates well-distributed maze patterns
- **Slower:** O(n²) expected time due to random walks
- **Memory:** Stores random walk paths in memory

**Use Cases:** Ideal when you want statistically uniform mazes and when balance of different maze patterns is important

**Example:**
```python
from mazegen import WilsonsGen, Maze

# Create a 50x50 maze using Wilson's Algorithm
maze = Maze(Point(50, 50))
gen = WilsonsGen(maze)
maze = gen.finish()
```

---

#### 3. Iterative Randomized Kruskal's (IRK)

**Overview:** IRK uses a union-find (disjoint set) data structure to track connected maze regions. It processes a randomized list of walls, opening only those that connect separate regions, until all regions merge into one connected maze.

**How It Works:**

1. Create a randomized list of all potential walls (each wall candidate listed only once)
2. Initialize each cell as its own component in a union-find structure
3. While walls remain:
   - Take a random wall from the list
   - If the wall's two neighboring cells are already connected, skip it
   - If the wall's cells are in separate components:
     - Open the wall (carve passage)
     - Union the two components
4. Continue until all cells form one connected component

**Characteristics:**
- **Elegant:** Clean mathematical approach using set theory
- **Perfect Guarantee:** Always produces perfect mazes
- **Uniform Distribution:** Each spanning tree equally likely
- **Efficient:** Nearly linear time due to union-find's O(α(n)) amortized cost
- **Balanced Texture:** Creates well-distributed patterns

**Use Cases:** When you want guaranteed optimality with near-linear performance, research applications

**Example:**
```python
from mazegen import IRK_Gen, Maze

# Create a 50x50 maze using Iterative Randomized Kruskal's
maze = Maze(Point(50, 50))
gen = IRK_Gen(maze)
maze = gen.finish()
```

---

#### Comparison Table

| Algorithm | Time | Perfect? | Texture | Distribution | Use Case |
|-----------|------|----------|---------|--------------|----------|
| **DFS** | O(n) | ✓ | Long corridors | Non-uniform | Fast, simple generation |
| **Wilson's** | O(n²) expected | ✓ | Balanced | Uniform | Statistically perfect |
| **IRK** | O(n × α(n)) | ✓ | Balanced | Uniform | Optimal performance |

### Pathfinding Algorithms

#### 1. Breadth-First Search (BFS)

**Overview:** BFS explores the maze level-by-level from the entry point, guaranteeing discovery of the shortest path. It explores all cells at distance k before exploring cells at distance k+1.

**How It Works:**

1. Start at entry point, add to queue and mark visited
2. While queue not empty:
   - Take cell from front of queue
   - If it's the exit, reconstruct and return path
   - For each neighboring cell with open passage:
     - If not visited and in bounds:
       - Mark as visited
       - Record current cell as parent
       - Add to queue for later exploration
3. Reconstruct path by following parent pointers backward

**Characteristics:**
- **Guaranteed Optimal:** Always finds shortest path
- **Simple:** Easy to understand and implement
- **Complete:** Will always find a solution if one exists
- **Memory Intensive:** May explore many cells in wide mazes
- **No Heuristic:** Explores without direction toward goal

**Complexity:**
- **Time:** O(w × h) - visits each cell once
- **Space:** O(w × h) - queue, visited set, parent pointers

**Use Cases:** When you need guaranteed shortest path, educational purposes, small to medium mazes

**Example:**
```python
from mazegen import DFSGen, BFSPathfinder, Point, Maze

maze = Maze(size=Point(20, 20), entry=Point(0, 0), exit=Point(0, 0))
maze = DFSGen(maze).finish()
pathfinder = BFSPathfinder(maze)
path = pathfinder.finish()

print(f"Shortest path: {len(path)} steps")
```

---

#### 2. A* Search

**Overview:** A* is an informed search algorithm that uses a heuristic function to guide exploration toward the goal. It balances the cost from the start with estimated cost to the goal, typically exploring far fewer cells than BFS while still guaranteeing the shortest path. For distance calculation, the estimated
distance from a point being evaluated to the exit point is added to its
distance from the entry point (explained in more detail below).

**How It Works:**

1. Calculate Manhattan distance heuristic from start to goal
2. Add start cell to open set with f-score = 0 + heuristic
3. While open set not empty:
   - Pop cell with lowest f-score
   - If it's the exit, reconstruct and return path
   - For each neighboring cell with open passage:
     - Skip if already explored or out of bounds
     - Calculate cost from start through current cell (g-score)
     - If this path is better than previous best path to neighbor:
       - Update parent and cost information
       - Calculate f-score = g-score + heuristic (estimated distance to exit)
       - Add to open set for future exploration

**Heuristic Function (Manhattan Distance):**
```
h(cell) = |cell.x - goal.x| + |cell.y - goal.y|
```
This heuristic is **admissible** (never overestimates actual distance), guaranteeing optimal paths.

**Characteristics:**
- **Optimal & Efficient:** Finds shortest path while exploring fewer cells
- **Heuristic Guided:** Intelligently directs search toward goal
- **Practical:** Dramatically faster than BFS in most cases
- **Flexible:** Heuristic can be tuned for different maze types
- **Slightly Complex:** More code than BFS
- **Heuristic Dependent:** Performance depends on heuristic quality

**Complexity:**
- **Time:** O(w × h) worst case, typically much better with good heuristic
- **Space:** O(w × h) - priority queue, sets, and score dictionaries

**Use Cases:** General purpose pathfinding, large mazes, performance-critical applications

**Example:**
```python
from mazegen import DFSGen, AStarPathfinder, Point

maze = Maze(size=Point(100, 100), entry=Point(0, 0), exit=Point(99, 99))
maze = DFSGen(maze).finish()
pathfinder = AStarPathfinder(maze)
path = pathfinder.finish()

print(f"A* found path: {len(path)} steps")
```

---

#### Comparison Table

| Algorithm | Optimality | Speed | Memory | Best For |
|-----------|-----------|-------|--------|----------|
| **BFS** | ✓ Guaranteed | Slow-Medium | High | Small mazes, education |
| **A*** | ✓ Guaranteed | Fast | Medium | Large mazes, production |

### API Reference

#### Maze Generators

All generators inherit from `MazeGenerator` base class and support step-by-step generation. The `MazeGenerator` base class already has the maze braiding method.

##### `DFSGen(maze, perfect=True, seed=None)`
Randomized Depth-First Search maze generator.
- **Parameters:**
  - `maze`: Maze object
  - `perfect`: If True, creates perfect maze; if False, removes dead ends (default: True)
  - `rand`: Random seed for reproducibility or Random class object (optional)

##### `WilsonsGen(width, height, seed=None)`
Wilson's Algorithm maze generator (always creates perfect mazes).
- **Parameters:**
  - `maze`: Maze object
  - `perfect`: If True, creates perfect maze; if False, removes dead ends (default: True)
  - `rand`: Random seed for reproducibility or Random class object (optional)

##### `IRK_Gen(width, height, perfect=True, seed=None)`
Iterative Randomized Kruskal's maze generator.
- **Parameters:**
  - `maze`: Maze object
  - `perfect`: If True, creates perfect maze; if False, removes dead ends (default: True)
  - `rand`: Random seed for reproducibility or Random class object (optional)

#### Generator Methods

```python
gen = DFSGen(maze)

# Step-by-step generation (for visualization)
while not gen.is_done():
    gen.next()  # Perform one generation step

# Get the finished maze
maze = gen.finish()

# Or generate in one call
maze = DFSGen(maze).finish()
```

#### Pathfinders

All pathfinders inherit from `Pathfinder` base class and support step-by-step pathfinding.

##### `BFSPathfinder(maze)`
Breadth-First Search pathfinder (guaranteed shortest path).

##### `AStarPathfinder(maze)`
A* Search pathfinder (guaranteed shortest path, typically faster).

#### Pathfinder Methods

```python
from mazegen import Point

pathfinder = BFSPathfinder(maze)

# Step-by-step pathfinding (for visualization)
while not pathfinder.is_done():
    pathfinder.next()  # Perform one pathfinding step

# Get the found path
path = pathfinder.get_path()

# Or find path in one call
path = BFSPathfinder(maze).finish()
```

#### Core Classes

##### `Maze`
Represents a complete maze structure.
- **Properties:**
  - `size`: named tuple Point descripting width (x) and height (y) of the maze
  - `entry`: entry point coordinates
  - `exit`: exit point coordinates
  - `grid`: 2D array of Cell objects

##### `Cell`
Represents a single maze cell.
- **Properties:**
  - `walls`: Bitmask indicating which walls are present
  - `visited`: Whether cell has been visited during generation
  - `lock`: Whether cell is locked

##### `Point(x, y)`
Simple 2D coordinate representation for positions in the maze.

##### `Wall`
Enumeration for wall directions: `NORTH`, `EAST`, `SOUTH`, `WEST`
2^4 bit mask is used, allowing for each cell's walls attribute to be
represented as a hex digit. The above directions' walls are represented
in bits in positions of 0 to 3 of the bit mask.

### Requirements

- Python >= 3.13
- disjoint-set >= 0.9.0

### Performance Tips

1. **For Large Mazes:** Use A* pathfinding instead of BFS
2. **For Visual Generation:** Use `next()` method with step-by-step generation
3. **For Reproducibility:** Provide `rand` parameter to generators
4. **For Balanced Mazes:** Use Wilson's or IRK algorithms
5. **For Speed:** Use DFS algorithm

### License

MIT License - See [LICENSE.md](LICENSE.md) for details

### Authors

- Mateusz Sowiński
- Aman Suleimenov

(End of the `mazegen` package documentation)

------------------------------------------------------------


## Instructions

### Prerequisites

- Python 3.13 or later
- `uv` for dependency and workspace management
- local `mlx` wheel stored in `lib/`

### Installation and setup

From the project root:

```bash
make install
```

This installs the workspace dependencies and makes the local `mazegen` package available to the application environment.

### Run the application

```bash
make run
```
or
```bash
uv run a_maze_ing.py config.txt
```

### Build and install the library wheel

```bash
cd /home/aman/42/A-Maze-ing/mazegen
uv build --package=mazegen
python -m pip install --force-reinstall ./dist/mazegen-*.whl
```

After installation, the package can be used as:

```python
from mazegen import DFSGen, BFSPathfinder, Maze, Point
```

### Run tests quickly

```bash
make pytest-fast
```

For more detail, use:

```bash
make pytest-verbose
```

### Linting

```bash
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

# seed for maze generation, can be int, string, none or omitted
SEED=42

# algorithm for maze generation
# available: dfs, wilson, irk
# default: dfs
MAZEGEN=dfs

# pathfinding algorithm
# available: bfs, astar
# default: bfs
PATHFINDING=bfs
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

### Anticipation

Orginal plan was to have simple program with animated generation and pathfinding of the maze,
later we added ability to skip animation and rerun with new random seed or with the old one.

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
