"""Tests for mazegen.util module."""

import pytest
from mazegen.util import Point


class TestPoint:
    """Test cases for Point class."""

    def test_point_creation(self) -> None:
        """Test creating a Point with x and y coordinates."""
        p: Point = Point(3, 5)
        assert p.x == 3
        assert p.y == 5

    def test_point_zero(self) -> None:
        """Test creating a Point at origin."""
        p: Point = Point(0, 0)
        assert p.x == 0
        assert p.y == 0

    def test_point_negative_coordinates(self) -> None:
        """Test creating a Point with negative coordinates."""
        p: Point = Point(-10, -20)
        assert p.x == -10
        assert p.y == -20

    def test_point_equality(self) -> None:
        """Test Point equality comparison."""
        p1: Point = Point(3, 5)
        p2: Point = Point(3, 5)
        p3: Point = Point(4, 5)

        assert p1 == p2
        assert p1 != p3

    def test_point_immutability(self) -> None:
        """Test that Point is immutable."""
        p: Point = Point(3, 5)
        with pytest.raises(AttributeError):
            object.__setattr__(p, "x", 10)

    def test_point_hashable(self) -> None:
        """Test that Point can be used in sets and as dict keys."""
        p1: Point = Point(3, 5)
        p2: Point = Point(3, 5)
        p3: Point = Point(4, 5)

        point_set: set[Point] = {p1, p2, p3}
        assert len(point_set) == 2

        point_dict: dict[Point, str] = {p1: "first", p3: "third"}
        assert point_dict[p2] == "first"

    def test_point_unpacking(self) -> None:
        """Test that Point can be unpacked."""
        p: Point = Point(7, 11)
        x: int
        y: int
        x, y = p
        assert x == 7
        assert y == 11

    def test_point_tuple_behavior(self) -> None:
        """Test that Point behaves like a tuple."""
        p: Point = Point(3, 5)
        assert p[0] == 3
        assert p[1] == 5
        assert len(p) == 2

    def test_point_iteration(self) -> None:
        """Test that Point can be iterated."""
        p: Point = Point(2, 8)
        coords: list[int] = list(p)
        assert coords == [2, 8]

    def test_point_repr(self) -> None:
        """Test Point string representation."""
        p: Point = Point(3, 5)
        assert "Point" in repr(p) or "x=3" in repr(p)

    def test_point_large_coordinates(self) -> None:
        """Test Point with large coordinates."""
        p: Point = Point(1000000, 2000000)
        assert p.x == 1000000
        assert p.y == 2000000

    def test_point_in_list(self) -> None:
        """Test Point in list operations."""
        points: list[Point] = [Point(1, 1), Point(2, 2), Point(3, 3)]
        assert Point(2, 2) in points
        assert Point(5, 5) not in points

    def test_point_equality_with_tuple(self) -> None:
        """Test Point equality with regular tuple."""
        p: Point = Point(3, 5)
        assert p == (3, 5)
        assert (3, 5) == p
