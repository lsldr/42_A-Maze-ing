# mazegen

A Python library for generating and solving mazes using multiple algorithms. mazegen provides efficient implementations of popular maze generation and pathfinding algorithms with both perfect and braided maze support.

## Features

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

## Installation

- *First, Ensure you downloaded the .whl or built it from the cloned repository*

```bash
pip install mazegen
```

## Quick Start

```python
from mazegen import DFSGen, BFSPathfinder, Point, Maze
from random import Random()

# Generate a maze using Depth-First Search
maze = Maze(Point(20, 20), Point(0, 0), Point(19, 19))
generator = DFSGen(maze, Random())
generator.finish()

# Find the shortest path through the maze
pathfinder = BFSPathfinder(maze)
path = pathfinder.finish()

print(f"Maze generated! Found path of length: {len(path)}")

# Or generate step-by-step for visualization
maze = Maze(Point(20, 20), Point(0, 0), Point(19, 19))
generator = DFSGen(maze, Random())
while not generator.is_done():
    generator.next()  # Do one generation step
    # Update your GUI here

maze = generator.finish()
```

## Maze Generation Algorithms

### 1. Randomized Depth-First Search (DFS)

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
from random import Random

# Create a 50x50 perfect maze
maze = Maze(Point(50, 50), Point(0, 0), Point(40, 40))
gen = DFSGen(maze=maze, rand=Random(), perfect=True)
gen.finish()

# Or create a braided maze (with multiple solutions)
maze = Maze(Point(50, 50), Point(0, 0), Point(40, 40))
gen = DFSGen(maze=maze, rand=Random(), perfect=False)
maze = gen.finish()
```

---

### 2. Wilson's Algorithm

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
from random import Random

# Create a 50x50 maze using Wilson's Algorithm
maze()
gen = WilsonsGen(width=50, height=50)
maze = gen.generate()
```

---

### 3. Iterative Randomized Kruskal's (IRK)

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
from mazegen import IRK_Gen

# Create a 50x50 maze using Iterative Randomized Kruskal's
gen = IRK_Gen(width=50, height=50)
maze = gen.generate()
```

---

### Comparison Table

| Algorithm | Time | Perfect? | Texture | Distribution | Use Case |
|-----------|------|----------|---------|--------------|----------|
| **DFS** | O(n) | ✓ | Long corridors | Non-uniform | Fast, simple generation |
| **Wilson's** | O(n²) expected | ✓ | Balanced | Uniform | Statistically perfect |
| **IRK** | O(n × α(n)) | ✓ | Balanced | Uniform | Optimal performance |

## Pathfinding Algorithms

### 1. Breadth-First Search (BFS)

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
from mazegen import DFSGen, BFSPathfinder, Point

maze = DFSGen(width=20, height=20).generate()
pathfinder = BFSPathfinder(maze)
path = pathfinder.find_path(Point(0, 0), Point(19, 19))

print(f"Shortest path: {len(path)} steps")
```

---

### 2. A* Search

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

maze = DFSGen(width=100, height=100).generate()
pathfinder = AStarPathfinder(maze)
path = pathfinder.find_path(Point(0, 0), Point(99, 99))

print(f"A* found path: {len(path)} steps")
```

---

### Comparison Table

| Algorithm | Optimality | Speed | Memory | Best For |
|-----------|-----------|-------|--------|----------|
| **BFS** | ✓ Guaranteed | Slow-Medium | High | Small mazes, education |
| **A*** | ✓ Guaranteed | Fast | Medium | Large mazes, production |

## API Reference

### Maze Generators

All generators inherit from `MazeGenerator` base class and support step-by-step generation. The `MazeGenerator` base class already has the maze braiding method.

#### `DFSGen(width, height, perfect=True, seed=None)`
Randomized Depth-First Search maze generator.
- **Parameters:**
  - `width`: Maze width in cells
  - `height`: Maze height in cells
  - `perfect`: If True, creates perfect maze; if False, removes dead ends (default: True)
  - `seed`: Random seed for reproducibility (optional)

#### `WilsonsGen(width, height, seed=None)`
Wilson's Algorithm maze generator (always creates perfect mazes).
- **Parameters:**
  - `width`: Maze width in cells
  - `height`: Maze height in cells
  - `seed`: Random seed for reproducibility (optional)

#### `IRK_Gen(width, height, perfect=True, seed=None)`
Iterative Randomized Kruskal's maze generator.
- **Parameters:**
  - `width`: Maze width in cells
  - `height`: Maze height in cells
  - `perfect`: If True, creates perfect maze; if False, removes dead ends (default: True)
  - `seed`: Random seed for reproducibility (optional)

### Generator Methods

```python
gen = DFSGen(width=20, height=20)

# Step-by-step generation (for visualization)
while not gen.is_done():
    gen.next()  # Perform one generation step

# Get the finished maze
maze = gen.finish()

# Or generate in one call
maze = DFSGen(width=20, height=20).generate()
```

### Pathfinders

All pathfinders inherit from `Pathfinder` base class and support step-by-step pathfinding.

#### `BFSPathfinder(maze)`
Breadth-First Search pathfinder (guaranteed shortest path).

#### `AStarPathfinder(maze)`
A* Search pathfinder (guaranteed shortest path, typically faster).

### Pathfinder Methods

```python
from mazegen import Point

pathfinder = BFSPathfinder(maze)

# Step-by-step pathfinding (for visualization)
while not pathfinder.is_done():
    pathfinder.next()  # Perform one pathfinding step

# Get the found path
path = pathfinder.get_path()

# Or find path in one call
path = BFSPathfinder(maze).find_path(
    start=Point(0, 0),
    end=Point(19, 19)
)
```

### Core Classes

#### `Maze`
Represents a complete maze structure.
- **Properties:**
  - `width`: Maze width
  - `height`: Maze height
  - `cells`: 2D array of Cell objects

#### `Cell`
Represents a single maze cell.
- **Properties:**
  - `walls`: Bitmask indicating which walls are present
  - `visited`: Whether cell has been visited during generation
  - `lock`: Whether cell is locked (immutable during generation)

#### `Point(x, y)`
Simple 2D coordinate representation for positions in the maze.

#### `Wall`
Enumeration for wall directions: `NORTH`, `EAST`, `SOUTH`, `WEST`
2^4 bit mask is used, allowing for each cell's walls attribute to be
represented as a hex digit. The above directions' walls are represented
in bits in positions of 0 to 3 of the bit mask.

## Requirements

- Python >= 3.13
- disjoint-set >= 0.9.0

## Performance Tips

1. **For Large Mazes:** Use A* pathfinding instead of BFS
2. **For Visual Generation:** Use `next()` method with step-by-step generation
3. **For Reproducibility:** Provide `seed` parameter to generators
4. **For Balanced Mazes:** Use Wilson's or IRK algorithms
5. **For Speed:** Use DFS algorithm

## License

MIT License - See [LICENSE.md](LICENSE.md) for details

## Authors

- Mateusz Sowiński
- Aman Suleimenov
