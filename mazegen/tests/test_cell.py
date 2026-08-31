"""Tests for mazegen.cell module."""

import pytest
from mazegen.cell import Cell, Wall


class TestWall:
    """Test cases for Wall enum."""

    def test_wall_values(self):
        """Test Wall enum has expected values."""
        assert Wall.NORTH is not None
        assert Wall.EAST is not None
        assert Wall.SOUTH is not None
        assert Wall.WEST is not None
        assert Wall.NONE is not None

    def test_wall_bitwise_operations(self):
        """Test Wall enum supports bitwise operations."""
        # Test combining walls
        combined = Wall.NORTH | Wall.EAST
        assert (combined & Wall.NORTH) == Wall.NORTH
        assert (combined & Wall.EAST) == Wall.EAST
        assert (combined & Wall.SOUTH) == Wall.NONE

    def test_wall_contains_other_wall(self):
        """Test checking if wall combination contains a specific wall."""
        walls = Wall.NORTH | Wall.SOUTH
        assert (walls & Wall.NORTH) == Wall.NORTH
        assert (walls & Wall.EAST) == Wall.NONE

    def test_wall_get_direction(self):
        """Test Wall.get_direction() returns correct delta."""
        from mazegen.util import Point

        assert Wall.NORTH.get_direction() == Point(0, -1)
        assert Wall.SOUTH.get_direction() == Point(0, 1)
        assert Wall.EAST.get_direction() == Point(1, 0)
        assert Wall.WEST.get_direction() == Point(-1, 0)

    def test_wall_from_direction(self):
        """Test creating Wall from direction Point."""
        from mazegen.util import Point

        assert Wall.from_direction(Point(0, -1)) == Wall.NORTH
        assert Wall.from_direction(Point(0, 1)) == Wall.SOUTH
        assert Wall.from_direction(Point(1, 0)) == Wall.EAST
        assert Wall.from_direction(Point(-1, 0)) == Wall.WEST

    def test_wall_opposite(self):
        """Test Wall.opposite() returns correct opposite direction."""
        assert Wall.NORTH.opposite() == Wall.SOUTH
        assert Wall.SOUTH.opposite() == Wall.NORTH
        assert Wall.EAST.opposite() == Wall.WEST
        assert Wall.WEST.opposite() == Wall.EAST

    def test_wall_str_representation(self):
        """Test Wall string representation."""
        # Should return some hex representation
        north_str = str(Wall.NORTH)
        assert north_str is not None
        assert isinstance(north_str, str)

    def test_wall_all_combination(self):
        """Test combining all walls."""
        all_walls = Wall.NORTH | Wall.EAST | Wall.SOUTH | Wall.WEST
        assert (all_walls & Wall.NORTH) == Wall.NORTH
        assert (all_walls & Wall.EAST) == Wall.EAST
        assert (all_walls & Wall.SOUTH) == Wall.SOUTH
        assert (all_walls & Wall.WEST) == Wall.WEST


class TestCell:
    """Test cases for Cell class."""

    def test_cell_creation(self):
        """Test creating a Cell."""
        cell = Cell()
        assert cell is not None
        assert hasattr(cell, "walls")

    def test_cell_initial_state(self):
        """Test Cell starts with all walls intact."""
        cell = Cell()
        # All walls should be present initially
        assert (cell.walls & Wall.NORTH) != Wall.NONE
        assert (cell.walls & Wall.EAST) != Wall.NONE
        assert (cell.walls & Wall.SOUTH) != Wall.NONE
        assert (cell.walls & Wall.WEST) != Wall.NONE

    def test_cell_visited_flag(self):
        """Test Cell visited flag."""
        cell = Cell()
        assert hasattr(cell, "visited")
        assert cell.visited in (True, False)

    def test_cell_lock_flag(self):
        """Test Cell lock flag."""
        cell = Cell()
        assert hasattr(cell, "lock")
        assert not cell.lock

    def test_cell_open_wall(self):
        """Test opening a wall on a Cell."""
        cell = Cell()

        # Open north wall
        cell.open_wall(Wall.NORTH)

        # North wall should now be gone
        assert (cell.walls & Wall.NORTH) == Wall.NONE

        # Other walls should remain
        assert (cell.walls & Wall.EAST) != Wall.NONE
        assert (cell.walls & Wall.SOUTH) != Wall.NONE
        assert (cell.walls & Wall.WEST) != Wall.NONE

    def test_cell_open_multiple_walls(self):
        """Test opening multiple walls on a Cell."""
        cell = Cell()

        cell.open_wall(Wall.NORTH)
        cell.open_wall(Wall.EAST)

        assert (cell.walls & Wall.NORTH) == Wall.NONE
        assert (cell.walls & Wall.EAST) == Wall.NONE
        assert (cell.walls & Wall.SOUTH) != Wall.NONE
        assert (cell.walls & Wall.WEST) != Wall.NONE

    def test_cell_cannot_open_wall_when_locked(self):
        """Test that locked cells cannot have walls opened."""
        cell = Cell()
        cell.lock = True

        # Attempting to open a wall on a locked cell should raise an error
        with pytest.raises(ValueError):
            cell.open_wall(Wall.NORTH)

        # Walls should remain intact
        assert (cell.walls & Wall.NORTH) != Wall.NONE

    def test_cell_lock_prevents_wall_operations(self):
        """Test that locking a cell prevents wall modifications."""
        cell = Cell()
        cell.open_wall(Wall.NORTH)  # Should work
        assert (cell.walls & Wall.NORTH) == Wall.NONE

        cell.lock = True

        # Now trying to open another wall should fail
        with pytest.raises(ValueError):
            cell.open_wall(Wall.EAST)

        # But already-open walls should remain open
        assert (cell.walls & Wall.NORTH) == Wall.NONE
        # And other walls should remain closed
        assert (cell.walls & Wall.EAST) != Wall.NONE

    def test_cell_all_walls_can_be_opened(self):
        """Test that all four walls can be opened."""
        cell = Cell()

        cell.open_wall(Wall.NORTH)
        cell.open_wall(Wall.EAST)
        cell.open_wall(Wall.SOUTH)
        cell.open_wall(Wall.WEST)

        assert (cell.walls & Wall.NORTH) == Wall.NONE
        assert (cell.walls & Wall.EAST) == Wall.NONE
        assert (cell.walls & Wall.SOUTH) == Wall.NONE
        assert (cell.walls & Wall.WEST) == Wall.NONE

    def test_cell_wall_state_independent(self):
        """Test that multiple cells have independent wall states."""
        cell1 = Cell()
        cell2 = Cell()

        cell1.open_wall(Wall.NORTH)

        # cell2 should still have all walls
        assert (cell2.walls & Wall.NORTH) != Wall.NONE
        assert (cell1.walls & Wall.NORTH) == Wall.NONE
