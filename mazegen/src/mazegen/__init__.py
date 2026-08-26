from mazegen.cell import Cell, Wall
from mazegen.generator.dfs import DFS_gen
from mazegen.generator.maze_generator import Maze_Generator
from mazegen.maze import Maze, MazeError
from mazegen.pathfinder.bfs import BFS_pathfinder
from mazegen.pathfinder.pathfinder import Pathfinder
from mazegen.util import Point

# Expose all the needed classes and functions at the package level
__all__ = [
    "BFS_pathfinder",
    "Cell",
    "DFS_gen",
    "Maze",
    "MazeError",
    "Maze_Generator",
    "Pathfinder",
    "Point",
    "Wall",
]
