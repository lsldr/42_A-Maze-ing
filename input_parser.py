from pathlib import Path
from typing import Any, Dict, Set


class ConfigError(Exception):
    """Custom exception raised for in
    valid configuration files."""

    pass


def parse_config(file_path_str: str) -> Dict[str, Any]:
    """Parse and validate a maze configuration file.

    Checks relative to CWD first, then relative to the script's directory.
    """
    path = Path(file_path_str)
    if not path.is_file():
        #  See if there is a file in the dir where the script is
        #  pathlib overloads the `/`, allowing path adjoining
        path = Path(__file__).resolve().parent / file_path_str
        if not path.is_file():
            raise FileNotFoundError(f"Config file not found: {file_path_str}")

    seen_keys: Set[str] = set()
    raw_config: Dict[str, str] = {}

    with path.open("r", encoding="utf-8") as file:
        #  open() returns an iterable AND iterator file object that we can
        #  stream with standard stream buffers
        for line_num, line in enumerate(file, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ConfigError(f"Line {line_num}: missing '=': '{line}'")

            key, val = line.split("=", 1)
            val = val.split("#", 1)[0]  # Allowing for comments in config
            key, val = key.strip(), val.strip()

            if key in seen_keys:
                raise ConfigError(f"Line {line_num}: Duplicate key '{key}'")

            seen_keys.add(key)
            raw_config[key] = val

    required_keys = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    }
    missing = required_keys - seen_keys
    if missing:
        raise ConfigError(f"Missing required configuration keys: {missing}")

    try:
        width = int(raw_config["WIDTH"])
        height = int(raw_config["HEIGHT"])
        if width < 3 or height < 3:
            raise ConfigError("WIDTH and HEIGHT must be at least 3")

        entry_x, entry_y = map(int, raw_config["ENTRY"].split(","))
        exit_x, exit_y = map(int, raw_config["EXIT"].split(","))

        if not (0 <= entry_x < width and 0 <= entry_y < height):
            raise ConfigError("ENTRY coordinates are out of bounds!")
        if not (0 <= exit_x < width and 0 <= exit_y < height):
            raise ConfigError("EXIT coordinates are out of bounds!")
        if (entry_x, entry_y) == (exit_x, exit_y):
            raise ConfigError("ENTRY and EXIT must be different points!")
        if width >= 9 and height >= 7:
            # 7x5 pattern centered on the grid
            start_x = (width - 7) // 2
            start_y = (height - 5) // 2

            # Occupied relative (dx, dy) coordinates within the 7x5 box
            pattern_42_offsets = {
                # "4" (columns 0..2)
                (0, 0),
                (0, 1),
                (0, 2),
                (1, 2),
                (2, 2),
                (2, 3),
                (2, 4),
                # "2" (columns 4..6)
                (4, 0),
                (5, 0),
                (6, 0),
                (6, 1),
                (6, 2),
                (5, 2),
                (4, 2),
                (4, 3),
                (4, 4),
                (5, 4),
                (6, 4),
            }

            pattern_cells = {
                (start_x + dx, start_y + dy) for dx, dy in pattern_42_offsets
            }

            if (entry_x, entry_y) in pattern_cells:
                raise ConfigError(
                    "ENTRY coordinates fall on the '42' pattern!"
                )
            if (exit_x, exit_y) in pattern_cells:
                raise ConfigError("EXIT coordinates fall on the '42' pattern!")

        perfect_raw = raw_config["PERFECT"].lower()
        if perfect_raw not in ("true", "false"):
            raise ConfigError(
                "PERFECT must be 'True' or 'False' (case insensitive)"
            )
        perfect = perfect_raw == "true"

    except ValueError as err:
        raise ConfigError(
            f"Type conversion error in config values: {err}"
        ) from err

    # Construct final config dictionary for mazegen
    return {
        "width": width,
        "height": height,
        "entry": (entry_x, entry_y),
        "exit": (exit_x, exit_y),
        "output_file": raw_config["OUTPUT_FILE"],
        "perfect": perfect,
        "pattern_cells": pattern_cells,
        **{
            k.lower(): v
            for k, v in raw_config.items()
            if k not in required_keys
        },
    }
