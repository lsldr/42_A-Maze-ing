from mazegen.cell import Cell, Wall
from mazegen.maze import Maze, MazeError
from mazegen.util import Point
from mazegen.generator.maze_generator import Maze_Generator
from mazegen.generator.dfs import DFS_gen
from mazegen.pathfinder.pathfinder import Pathfinder
from mazegen.pathfinder.bfs import BFS_pathfinder
from mazegen.input_parser import parse_config, ConfigError

# Expose all the needed classes and functions at the package level
__all__ = [
    "Cell",
    "Wall",
    "Maze",
    "MazeError",
    "Point",
    "Maze_Generator",
    "DFS_gen",
    "Pathfinder",
    "BFS_pathfinder",
    "parse_config",
    "ConfigError",
]
