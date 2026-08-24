import sys
from gui.program import Program
from mazegen.input_parser import ConfigError, parse_config


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
        print(config_dict)
        Program().run()
    except (FileNotFoundError, ConfigError) as e:
        print(f"Error parsing configs with the provided filename:\n{e}")


if __name__ == "__main__":
    main()
