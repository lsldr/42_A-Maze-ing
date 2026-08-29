from pathlib import Path

from input_parser import parse_config


def test_parse_config_accepts_a_star_pathfinding_alias(tmp_path: Path) -> None:
    config = tmp_path / "config_astar.txt"
    config.write_text(
        "WIDTH=10\n"
        "HEIGHT=10\n"
        "ENTRY=1,1\n"
        "EXIT=8,8\n"
        "OUTPUT_FILE=maze.txt\n"
        "PERFECT=False\n"
        "PATHFINDING=a_star\n",
        encoding="utf-8",
    )

    parsed = parse_config(str(config))

    assert parsed["pathfinding"] == "astar"
