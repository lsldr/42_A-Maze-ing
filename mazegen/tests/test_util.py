"""Tests for mazegen.util module."""

import pytest
from mazegen.util import Point


class TestPoint:
    """Test cases for Point class."""

    def test_point_creation(self):
        """Test creating a Point with x and y coordinates."""
        p = Point(3, 5)
        assert p.x == 3
        assert p.y == 5

    def test_point_zero(self):
        """Test creating a Point at origin."""
        p = Point(0, 0)
        assert p.x == 0
        assert p.y == 0

    def test_point_negative_coordinates(self):
        """Test creating a Point with negative coordinates."""
        p = Point(-10, -20)
        assert p.x == -10
        assert p.y == -20

    def test_point_equality(self):
        """Test Point equality comparison."""
        p1 = Point(3, 5)
        p2 = Point(3, 5)
        p3 = Point(4, 5)

        assert p1 == p2
        assert p1 != p3

    def test_point_immutability(self):
        """Test that Point is immutable."""
        p = Point(3, 5)
        with pytest.raises(AttributeError):
            p.x = 10

    def test_point_hashable(self):
        """Test that Point can be used in sets and as dict keys."""
        p1 = Point(3, 5)
        p2 = Point(3, 5)
        p3 = Point(4, 5)

        # Can be used in a set
        point_set = {p1, p2, p3}
        assert len(point_set) == 2  # p1 and p2 should be the same

        # Can be used as dict key
        point_dict = {p1: "first", p3: "third"}
        assert point_dict[p2] == "first"  # p2 should match p1

    def test_point_unpacking(self):
        """Test that Point can be unpacked."""
        p = Point(7, 11)
        x, y = p
        assert x == 7
        assert y == 11

    def test_point_tuple_behavior(self):
        """Test that Point behaves like a tuple."""
        p = Point(3, 5)
        assert p[0] == 3
        assert p[1] == 5
        assert len(p) == 2

    def test_point_iteration(self):
        """Test that Point can be iterated."""
        p = Point(2, 8)
        coords = list(p)
        assert coords == [2, 8]

    def test_point_repr(self):
        """Test Point string representation."""
        p = Point(3, 5)
        assert "Point" in repr(p) or "x=3" in repr(p)

    def test_point_large_coordinates(self):
        """Test Point with large coordinates."""
        p = Point(1000000, 2000000)
        assert p.x == 1000000
        assert p.y == 2000000

    def test_point_in_list(self):
        """Test Point in list operations."""
        points = [Point(1, 1), Point(2, 2), Point(3, 3)]
        assert Point(2, 2) in points
        assert Point(5, 5) not in points

    def test_point_equality_with_tuple(self):
        """Test Point equality with regular tuple."""
        p = Point(3, 5)
        assert p == (3, 5)
        assert (3, 5) == p
