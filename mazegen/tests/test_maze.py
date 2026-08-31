"""Tests for mazegen.maze module - FIXED VERSION."""

import pytest
from mazegen.maze import Maze
from mazegen.util import Point
from mazegen.cell import Wall


class TestMaze:
    """Test cases for Maze class."""

    def test_maze_creation(self) -> None:
        """Test creating a basic Maze."""
        maze: Maze = Maze(
            size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9)
        )
        assert maze is not None
        assert maze.size == Point(10, 10)
        assert maze.entry == Point(0, 0)
        assert maze.exit == Point(9, 9)

    def test_maze_dimensions(self) -> None:
        """Test Maze dimensions are correct."""
        maze: Maze = Maze(
            size=Point(20, 15), entry=Point(0, 0), exit=Point(19, 14)
        )
        assert maze.size.x == 20
        assert maze.size.y == 15

    def test_maze_entry_exit_validation(self) -> None:
        """Test that entry and exit must be within bounds."""
        size: Point = Point(10, 10)

        with pytest.raises(ValueError):
            Maze(size=size, entry=Point(10, 10), exit=Point(9, 9))

        with pytest.raises(ValueError):
            Maze(size=size, entry=Point(0, 0), exit=Point(10, 10))

    def test_maze_in_bounds(self) -> None:
        """Test in_bounds method."""
        maze: Maze = Maze(
            size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9)
        )

        assert maze.in_bounds(Point(0, 0))
        assert maze.in_bounds(Point(5, 5))
        assert maze.in_bounds(Point(9, 9))
        assert not maze.in_bounds(Point(-1, 5))
        assert not maze.in_bounds(Point(10, 5))
        assert not maze.in_bounds(Point(5, 10))

    def test_maze_get_cell(self) -> None:
        """Test getting a cell from the maze grid."""
        maze: Maze = Maze(
            size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9)
        )
        cell = maze.get_cell(Point(5, 5))
        assert cell is not None

    def test_maze_get_cell_bounds_check(self) -> None:
        """Test that get_cell validates bounds."""
        maze: Maze = Maze(
            size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9)
        )

        cell = maze.get_cell(Point(0, 0))
        assert cell is not None

        with pytest.raises(IndexError):
            maze.get_cell(Point(10, 10))

    def test_maze_pattern_cells(self) -> None:
        """Test that pattern_cells are locked."""
        pattern: set[Point] = {Point(5, 5), Point(6, 6)}
        maze: Maze = Maze(
            size=Point(10, 10),
            entry=Point(0, 0),
            exit=Point(9, 9),
            pattern_cells=pattern,
        )

        assert maze.get_cell(Point(5, 5)).lock
        assert maze.get_cell(Point(6, 6)).lock
        assert not maze.get_cell(Point(0, 0)).lock

    def test_maze_try_open_wall(self) -> None:
        """Test opening a wall between two cells."""
        maze: Maze = Maze(
            size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9)
        )

        result: bool = maze.try_open_wall(Point(5, 5), Wall.EAST)

        assert result
        cell1 = maze.get_cell(Point(5, 5))
        assert (cell1.walls & Wall.EAST) == Wall.NONE

    def test_maze_try_open_wall_locked_cell(self) -> None:
        """Test that try_open_wall fails on locked cells."""
        pattern: set[Point] = {Point(5, 5)}
        maze: Maze = Maze(
            size=Point(10, 10),
            entry=Point(0, 0),
            exit=Point(9, 9),
            pattern_cells=pattern,
        )

        result: bool = maze.try_open_wall(Point(5, 5), Wall.EAST)
        assert not result

    def test_maze_try_open_wall_out_of_bounds(self) -> None:
        """Test that try_open_wall handles out-of-bounds gracefully."""
        maze: Maze = Maze(
            size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9)
        )

        result: bool = maze.try_open_wall(Point(0, 0), Wall.WEST)
        assert not result

    def test_maze_count_open_passages(self) -> None:
        """Test counting open passages in a cell."""
        maze: Maze = Maze(
            size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9)
        )

        count: int = maze.count_open_passages(Point(5, 5))
        assert count == 0

        maze.try_open_wall(Point(5, 5), Wall.NORTH)
        count = maze.count_open_passages(Point(5, 5))
        assert count == 1

    def test_maze_path_property(self) -> None:
        """Test setting and getting maze path."""
        maze: Maze = Maze(
            size=Point(10, 10), entry=Point(0, 0), exit=Point(9, 9)
        )
        path: list[Point] = [Point(0, 0), Point(1, 0), Point(2, 0)]
        maze.path = path
        assert maze.path == path

    def test_maze_str_representation(self) -> None:
        """Test maze string representation."""
        maze: Maze = Maze(
            size=Point(5, 5), entry=Point(0, 0), exit=Point(4, 4)
        )
        maze_str: str = str(maze)
        assert isinstance(maze_str, str)
        assert len(maze_str) > 0
