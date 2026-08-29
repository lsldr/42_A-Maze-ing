from typing import NamedTuple


class Point(NamedTuple):
    """2D integer coordinate point.

    Attributes:
        x (int): Horizontal coordinate (column).
        y (int): Vertical coordinate (row).
    """

    x: int
    y: int
