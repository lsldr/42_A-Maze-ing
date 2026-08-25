import sys
from random import Random
from mazegen import (
    parse_config,
    ConfigError,
    Maze,
    Point,
    DFS_gen,
    BFS_pathfinder,
)

from gui.maze import MazeManager
from gui.menu import MainMenuPanel
from gui.program import Program
from mlx import Mlx
from PIL import Image

from typing import Any
import time


def loop_callback(prog: Program) -> None:
    """Callback for main application loop

    Args:
        prog (Program): object keeping the state of application
    """
    menu_width = prog.width // 4
    maze_border = 20
    maze_width = (prog.width - menu_width) - maze_border * 2
    maze_height = prog.height - maze_border * 2

    mlx = Mlx()

    # 1. Draw menu
    menu_ptr = mlx.mlx_new_image(prog.mlx_ptr, menu_width, prog.height)
    menu_data, _, _, _ = mlx.mlx_get_data_addr(menu_ptr)
    menu = Image.new(
        "RGBA", (menu_width, prog.height), "#181825"
    )  # Dark gray/blue background
    prog.active_menu.draw(menu)
    menu_data[:] = menu.tobytes()

    # 2. Draw maze
    maze_ptr = mlx.mlx_new_image(prog.mlx_ptr, maze_width, maze_height)
    maze_data, _, _, _ = mlx.mlx_get_data_addr(maze_ptr)
    maze = Image.new("RGBA", (maze_width, maze_height), 0xFFDDDDDD)
    prog.maze.tick(prog)
    prog.maze.draw(maze, prog)

    maze_data[:] = maze.tobytes()
    mlx.mlx_clear_window(prog.mlx_ptr, prog.win_ptr)
    mlx.mlx_put_image_to_window(
        prog.mlx_ptr, prog.win_ptr, menu_ptr, prog.width - menu_width, 0
    )
    mlx.mlx_put_image_to_window(
        prog.mlx_ptr, prog.win_ptr, maze_ptr, maze_border, maze_border
    )
    mlx.mlx_destroy_image(prog.mlx_ptr, menu_ptr)
    mlx.mlx_destroy_image(prog.mlx_ptr, maze_ptr)
    if prog.quit:
        mlx.mlx_loop_exit(prog.mlx_ptr)
    time.sleep(0.016)  # Around ~60 FPS


def keys_callback(key: int, prog: Program) -> None:
    """Callback for handling key input
    Only released key is send

    Args:
        key (int): keycode of pressed key
        prog (Program): object keeping the state of application
    """
    if key == 65307:
        prog.quit = True
    prog.active_menu.handle_keys(key, prog)


def expose_callback(prog: Program) -> None:
    """Callback for expose event

    Expose is called when X11 request repainting of the window

    Args:
        prog (Program): object keeping the state of application
    """
    # print("Expose")


def close_callback(prog: Program) -> None:
    """Callback for when the close button of the window was pressed

    Args:
        prog (Program): object kepping the state of application
    """
    Mlx().mlx_loop_exit(prog.mlx_ptr)


def run(config: dict[str, Any], grid: list[list[int]]) -> None:
    """Configure and start the application

    Creates window and start main application loop
    Will only return when application stop
    """
    width = 1440
    height = 810
    title = "A-Maze-Ing"

    mlx_obj = None
    mlx_ptr = None
    win_ptr = None
    try:
        mlx_obj = Mlx()
        mlx_ptr: int | None = mlx_obj.mlx_init()
        if not mlx_ptr:
            raise RuntimeError(
                "Failed to initialize MiniLibX (mlx_init returned NULL). "
                "Ensure your DISPLAY environment variable is set."
            )
        win_ptr: int | None = mlx_obj.mlx_new_window(
            mlx_ptr, width, height, title
        )
        if not win_ptr:
            raise RuntimeError(
                "Failed to create MiniLibX window "
                "(mlx_new_window returned NULL)."
            )

        main_menu = MainMenuPanel()
        maze_panel = MazeManager()

        prog = Program(
            mlx_ptr,
            win_ptr,
            config,
            grid,
            width,
            height,
            main_menu,
            maze_panel,
        )
        mlx_obj.mlx_key_hook(win_ptr, keys_callback, prog)
        mlx_obj.mlx_expose_hook(win_ptr, expose_callback, prog)
        mlx_obj.mlx_loop_hook(mlx_ptr, loop_callback, prog)
        mlx_obj.mlx_hook(win_ptr, 33, 0, close_callback, prog)
        mlx_obj.mlx_loop(mlx_ptr)
    except (OSError, RuntimeError, KeyboardInterrupt) as e:
        print(f"{e.__class__} error occurred: {e}", file=sys.stderr)
    finally:
        if mlx_obj and mlx_ptr:
            if win_ptr:
                mlx_obj.mlx_destroy_window(mlx_ptr, win_ptr)
            mlx_obj.mlx_release(mlx_ptr)


def main() -> None:
    if len(sys.argv) != 2:
        print(
            "Provide only 1 argument, which is a config file name:\n"
            "E.g.: `python3 a_maze_ing.py config.txt`",
            file=sys.stderr,
        )
        sys.exit(1)
    try:
        # parsing from the file provided to the `configs` dict
        configs = parse_config(sys.argv[1].strip())
    except (FileNotFoundError, ConfigError) as e:
        print(f"Error parsing configs with the provided filename:\n{e}")
        sys.exit()

    # Build the maze from configs
    size = Point(configs["width"], configs["height"])
    entry_pos = Point(*configs["entry"])
    exit_pos = Point(*configs["exit"])
    perfect = configs.get("perfect", True)

    maze = Maze(size, entry_pos, exit_pos)
    rng = Random()

    # Use the depth-first search generator
    dfs_generator = DFS_gen(maze, rng, perfect=perfect)
    dfs_generator.finish()

    # Print to check the maze
    print("\n--- Generated Maze ---")
    print(maze)
    print("----------------------\n")
    run(configs, maze.grid)


if __name__ == "__main__":
    main()
