"""Tests for mazegen maze generator modules - FIXED VERSION."""

from random import Random

from mazegen.maze import Maze
from mazegen.util import Point
from mazegen.generator.dfs import DFSGen
from mazegen.generator.wilsons import WilsonsGen
from mazegen.generator.irk import IRK_Gen


class TestDFSGen:
    """Test cases for DFSGen maze generator."""

    def test_dfs_gen_creation(self):
        """Test creating a DFSGen generator."""
        maze = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))
        gen = DFSGen(maze=maze, rand=Random(42), perfect=True)
        assert gen is not None
        assert gen.maze == maze

    def test_dfs_gen_generates_maze(self):
        """Test that DFSGen actually generates a maze."""
        maze = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))
        gen = DFSGen(maze=maze, rand=Random(42), perfect=True)

        result = gen.finish()
        assert result is not None
        assert result == maze

    def test_dfs_gen_creates_passages(self):
        """Test that DFSGen creates passages (opens walls)."""
        maze = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))
        gen = DFSGen(maze=maze, rand=Random(42), perfect=True)

        gen.finish()

        # After generation, at least some walls should be open
        open_passages = 0
        for x in range(10):
            for y in range(10):
                open_passages += maze.count_open_passages(Point(x, y))

        assert open_passages > 0

    def test_dfs_gen_seeded(self):
        """Test that DFSGen with same seed produces similar maze."""
        maze1 = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))
        gen1 = DFSGen(maze=maze1, rand=Random(42), perfect=True)
        gen1.finish()

        maze2 = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))
        gen2 = DFSGen(maze=maze2, rand=Random(42), perfect=True)
        gen2.finish()

        # With same seed, should generate identical maze structure
        for x in range(10):
            for y in range(10):
                cell1 = maze1.get_cell(Point(x, y))
                cell2 = maze2.get_cell(Point(x, y))
                assert cell1.walls == cell2.walls

    def test_dfs_gen_respects_pattern_cells(self):
        """Test that DFSGen respects locked pattern cells."""
        pattern = {Point(5, 5)}
        maze = Maze(
            size=Point(15, 15),
            entry=Point(0, 0),
            exit=Point(14, 14),
            pattern_cells=pattern,
        )
        gen = DFSGen(maze=maze, rand=Random(42), perfect=True)
        gen.finish()

        # Pattern cells should remain locked
        assert maze.get_cell(Point(5, 5)).lock


class TestWilsonsGen:
    """Test cases for WilsonsGen maze generator."""

    def test_wilsons_gen_creation(self):
        """Test creating a WilsonsGen generator."""
        maze = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))
        gen = WilsonsGen(maze=maze, rand=Random(42))
        assert gen is not None
        assert gen.maze == maze

    def test_wilsons_gen_generates_maze(self):
        """Test that WilsonsGen generates a maze."""
        maze = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))
        gen = WilsonsGen(maze=maze, rand=Random(42))

        result = gen.finish()
        assert result is not None
        assert result == maze

    def test_wilsons_gen_creates_passages(self):
        """Test that WilsonsGen creates passages."""
        maze = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))
        gen = WilsonsGen(maze=maze, rand=Random(42))

        gen.finish()

        open_passages = 0
        for x in range(10):
            for y in range(10):
                open_passages += maze.count_open_passages(Point(x, y))

        assert open_passages > 0

    def test_wilsons_gen_seeded(self):
        """Test that WilsonsGen with same seed produces similar maze."""
        maze1 = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))
        gen1 = WilsonsGen(maze=maze1, rand=Random(42))
        gen1.finish()

        maze2 = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))
        gen2 = WilsonsGen(maze=maze2, rand=Random(42))
        gen2.finish()

        # With same seed, should generate identical maze
        for x in range(10):
            for y in range(10):
                cell1 = maze1.get_cell(Point(x, y))
                cell2 = maze2.get_cell(Point(x, y))
                assert cell1.walls == cell2.walls


class TestIRKGen:
    """Test cases for IRK_Gen maze generator."""

    def test_irk_gen_creation(self):
        """Test creating an IRK_Gen generator."""
        maze = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))
        gen = IRK_Gen(maze=maze, rand=Random(42), perfect=True)
        assert gen is not None
        assert gen.maze == maze

    def test_irk_gen_generates_maze(self):
        """Test that IRK_Gen generates a maze."""
        maze = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))
        gen = IRK_Gen(maze=maze, rand=Random(42), perfect=True)

        result = gen.finish()
        assert result is not None
        assert result == maze

    def test_irk_gen_creates_passages(self):
        """Test that IRK_Gen creates passages."""
        maze = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))
        gen = IRK_Gen(maze=maze, rand=Random(42), perfect=True)

        gen.finish()

        open_passages = 0
        for x in range(10):
            for y in range(10):
                open_passages += maze.count_open_passages(Point(x, y))

        assert open_passages > 0

    def test_irk_gen_seeded(self):
        """Test that IRK_Gen with same seed produces similar maze."""
        maze1 = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))
        gen1 = IRK_Gen(maze=maze1, rand=Random(42), perfect=True)
        gen1.finish()

        maze2 = Maze(size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9))
        gen2 = IRK_Gen(maze=maze2, rand=Random(42), perfect=True)
        gen2.finish()

        # With same seed, should generate identical maze
        for x in range(10):
            for y in range(10):
                cell1 = maze1.get_cell(Point(x, y))
                cell2 = maze2.get_cell(Point(x, y))
                assert cell1.walls == cell2.walls


class TestGeneratorComparison:
    """Test comparing different generators."""

    def test_all_generators_produce_mazes(self):
        """Test that all three generators can produce mazes."""
        for GeneratorClass in [DFSGen, WilsonsGen, IRK_Gen]:
            maze = Maze(
                size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9)
            )
            gen = GeneratorClass(maze=maze, rand=Random(42), perfect=True)

            result = gen.finish()
            assert result is not None

            passages = sum(
                maze.count_open_passages(Point(x, y))
                for x in range(10)
                for y in range(10)
            )
            assert passages > 0

    def test_generators_with_small_maze(self):
        """Test that generators work with minimal maze size."""
        for GeneratorClass in [DFSGen, WilsonsGen, IRK_Gen]:
            maze = Maze(size=Point(3, 3), entry=Point(0, 0), exit=Point(2, 2))
            gen = GeneratorClass(maze=maze, rand=Random(42), perfect=True)

            result = gen.finish()
            assert result is not None
