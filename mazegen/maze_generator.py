from typing import Dict, Any


def grid_builder(configs: Dict[str, Any]) -> list[list[int]]:
    grid = list[list[int]]
    print(configs)

    grid = list([[15] * configs.get("width")] * configs.get("height"))

    print(grid)
    return grid
