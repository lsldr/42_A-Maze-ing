Choices:
  Project tools:
  - module manager: *uv*
  - docstring style: Google
  - Visuals: minilibx


  Algorithms:
  - Mazegen algos: 
                Randomized Depth-First Search (1)
                Randomized Kruskal’s Algorithm (2)
  - Pathfinding algos:
                Breadth-First Search (1)
                A* Search (2)
  - Wall removal strategy:
                On a perfect tree, open 4 corners and center, then remove 
                some dead ends (maybe a %) to have >=2 loops

                No dead ends: iterate until dead ends remain and remove walls
                adjacent to valid paths. Avoid 3*3 spaces while doing this.
