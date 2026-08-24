import sys
from gui.program import Program
from mazegen.input_parser import ConfigError, parse_config
from mazegen.maze_generator import dfs_maze_gen


def main() -> None:
    if len(sys.argv) != 2:
        print(
            "Provide only 1 argument, which is a config file name:\n"
            "E.g.: `python3 a_maze_ing.py config.txt`",
            file=sys.stderr,
        )
        sys.exit(1)
    try:
        config_dict = parse_config(sys.argv[1].strip())
        grid = dfs_maze_gen(config_dict)

        # Launch GUI with the parsed configuration and generated maze
        Program(config=config_dict, grid=grid).run()

    except (FileNotFoundError, ConfigError) as e:
        print(f"Error parsing configs with the provided filename:\n{e}")


if __name__ == "__main__":
    main()
