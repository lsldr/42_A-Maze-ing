"""Tests for mazegen pathfinder modules - FIXED VERSION."""

from random import Random

from mazegen.maze import Maze
from mazegen.util import Point
from mazegen.generator.dfs import DFSGen
from mazegen.pathfinder.bfs import BFSPathfinder
from mazegen.pathfinder.astar import AStarPathfinder
from mazegen.cell import Wall


class TestBFSPathfinder:
    """Test cases for BFSPathfinder."""

    def test_bfs_pathfinder_creation(self):
        """Test creating a BFSPathfinder."""
        maze = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))
        pathfinder = BFSPathfinder(maze=maze)
        assert pathfinder is not None
        assert pathfinder.maze == maze

    def test_bfs_find_path_simple(self):
        """Test BFS finding path in a generated maze."""
        maze = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))

        gen = DFSGen(maze=maze, rand=Random(42), perfect=True)
        gen.finish()

        pathfinder = BFSPathfinder(maze=maze)
        path = pathfinder.finish()

        assert path is not None
        assert len(path) > 0
        assert path[0] == maze.entry
        assert path[-1] == maze.exit

    def test_bfs_path_continuity(self):
        """Test that BFS path is continuous (adjacent cells)."""
        maze = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))

        gen = DFSGen(maze=maze, rand=Random(42), perfect=True)
        gen.finish()

        pathfinder = BFSPathfinder(maze=maze)
        path = pathfinder.finish()

        for i in range(len(path) - 1):
            current = path[i]
            next_point = path[i + 1]
            distance = abs(current.x - next_point.x) + abs(
                current.y - next_point.y
            )
            assert distance == 1

    def test_bfs_is_done_flag(self):
        """Test BFS is_done flag."""
        maze = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))

        gen = DFSGen(maze=maze, rand=Random(42), perfect=True)
        gen.finish()

        pathfinder = BFSPathfinder(maze=maze)

        assert not pathfinder.is_done()

        pathfinder.finish()

        assert pathfinder.is_done()

    def test_bfs_get_path(self):
        """Test getting the path from pathfinder."""
        maze = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))

        gen = DFSGen(maze=maze, rand=Random(42), perfect=True)
        gen.finish()

        pathfinder = BFSPathfinder(maze=maze)
        pathfinder.finish()

        path = pathfinder.get_path()
        assert path is not None
        assert len(path) > 0


class TestAStarPathfinder:
    """Test cases for AStarPathfinder."""

    def test_astar_pathfinder_creation(self):
        """Test creating an AStarPathfinder."""
        maze = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))
        pathfinder = AStarPathfinder(maze=maze)
        assert pathfinder is not None
        assert pathfinder.maze == maze

    def test_astar_find_path_simple(self):
        """Test A* finding path in a generated maze."""
        maze = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))

        gen = DFSGen(maze=maze, rand=Random(42), perfect=True)
        gen.finish()

        pathfinder = AStarPathfinder(maze=maze)
        path = pathfinder.finish()

        assert path is not None
        assert len(path) > 0
        assert path[0] == maze.entry
        assert path[-1] == maze.exit

    def test_astar_path_continuity(self):
        """Test that A* path is continuous."""
        maze = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))

        gen = DFSGen(maze=maze, rand=Random(42), perfect=True)
        gen.finish()

        pathfinder = AStarPathfinder(maze=maze)
        path = pathfinder.finish()

        for i in range(len(path) - 1):
            current = path[i]
            next_point = path[i + 1]
            distance = abs(current.x - next_point.x) + abs(
                current.y - next_point.y
            )
            assert distance == 1

    def test_astar_is_done_flag(self):
        """Test A* is_done flag."""
        maze = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))

        gen = DFSGen(maze=maze, rand=Random(42), perfect=True)
        gen.finish()

        pathfinder = AStarPathfinder(maze=maze)

        assert not pathfinder.is_done()

        pathfinder.finish()

        assert pathfinder.is_done()


class TestPathfinderComparison:
    """Test comparing different pathfinders."""

    def test_both_pathfinders_find_same_length_path(self):
        """Test that both pathfinders find paths of same length."""
        # Create same maze twice with same seed
        maze1 = Maze(size=Point(15, 15), entry=Point(0, 0), exit=Point(14, 14))
        gen1 = DFSGen(maze=maze1, rand=Random(42), perfect=True)
        gen1.finish()

        bfs_pathfinder = BFSPathfinder(maze=maze1)
        bfs_path = bfs_pathfinder.finish()

        # Generate same maze structure with same seed
        maze2 = Maze(size=Point(15, 15), entry=Point(0, 0), exit=Point(14, 14))
        gen2 = DFSGen(maze=maze2, rand=Random(42), perfect=True)
        gen2.finish()

        astar_pathfinder = AStarPathfinder(maze=maze2)
        astar_path = astar_pathfinder.finish()

        # Both should find paths of same length (optimal)
        assert len(bfs_path) == len(astar_path)

    def test_pathfinders_on_simple_maze(self):
        """Test pathfinders on a simple manually-created maze."""
        maze = Maze(size=Point(3, 3), entry=Point(0, 0), exit=Point(2, 0))

        # Create a simple straight line: (0,0) -> (1,0) -> (2,0)
        maze.try_open_wall(Point(0, 0), Wall.EAST)
        maze.try_open_wall(Point(1, 0), Wall.EAST)

        for PathfinderClass in [BFSPathfinder, AStarPathfinder]:
            pathfinder = PathfinderClass(maze=maze)
            path = pathfinder.finish()

            assert path is not None
            assert len(path) == 3
            assert path == [Point(0, 0), Point(1, 0), Point(2, 0)]
