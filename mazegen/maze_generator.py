from typing import Dict, Any
from random import randint


def grid_builder(configs: Dict[str, Any]) -> list[list[int]]:
    grid = list[list[int]]
    print(configs)
    w = configs.get("width")
    h = configs.get("height")

    grid = list([[15] * w] * h)

    if w >= 9 or h >= 7:
        immutable = block_ft_pattern(grid)
    else:
        print(
            "Warning: maze dimensions are too small for the 42 pattern!\n"
            "Generating a maze without the 42 pattern."
        )

    print(grid)
    return grid


def block_ft_pattern(grid: list[list[int]]) -> set[tuple[int, int]]:
    immutable = set()
