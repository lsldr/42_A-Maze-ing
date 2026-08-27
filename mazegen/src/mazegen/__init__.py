from mazegen.cell import Cell, Wall
from mazegen.generator.dfs import DFSGen
from mazegen.generator.maze_generator import MazeGenerator
from mazegen.generator.wilsons import WilsonsGen
from mazegen.maze import Maze, MazeError
from mazegen.pathfinder.bfs import BFSPathfinder
from mazegen.pathfinder.pathfinder import Pathfinder
from mazegen.util import Point

# Expose all the needed classes and functions at the package level
__all__ = [
    "BFSPathfinder",
    "Cell",
    "DFSGen",
    "Maze",
    "MazeError",
    "MazeGenerator",
    "Pathfinder",
    "Point",
    "Wall",
    "WilsonsGen"
]
