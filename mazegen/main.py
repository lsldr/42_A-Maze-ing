import sys
from input_parser import parse_config, ConfigError


def main():
    print("Hello from mazegen!")
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
    except (FileNotFoundError, ConfigError) as e:
        print(f"Error parsing configs with the provided filename:\n{e}")


if __name__ == "__main__":
    main()
