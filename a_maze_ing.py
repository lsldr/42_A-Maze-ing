import sys
from mazegen.input_parser import ConfigError, parse_config
from mazegen.maze_generator import dfs_maze_gen, print_maze


def main() -> None:
    print("Hello from a-maze-ing!")
    if len(sys.argv) != 2:
        print(
            "Provide only 1 argument, which is a config file name:\n"
            "E.g.: `python3 a_maze_ing.py config.txt`",
            file=sys.stderr,
        )
        sys.exit(1)
    try:
        config_dict = parse_config(sys.argv[1].strip())

        # 1. Generate the maze
        grid = dfs_maze_gen(config_dict)

        # 2. Print ASCII maze to terminal
        print("\nGenerated Maze:")
        print_maze(grid, config_dict["width"], config_dict["height"])
        print()

        # 3. Launch GUI (or check config_dict.get("gui"))
        # Program().run()

    except (FileNotFoundError, ConfigError) as e:
        print(f"Error parsing configs with the provided filename:\n{e}")


if __name__ == "__main__":
    main()
