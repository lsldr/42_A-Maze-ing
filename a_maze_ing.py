import sys
import time
from gui.program import Program
from input_parser import ConfigError, parse_config
from mlx import Mlx
from PIL import Image
from typing import Any


def loop_callback(prog: Program) -> None:
    """Callback for main application loop

    Args:
        prog (Program): object keeping the state of application
    """
    timestart = time.perf_counter()
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
    maze = Image.new("RGBA", (maze_width, maze_height))
    prog.maze_panel.tick(prog)
    prog.maze_panel.draw(maze, prog)

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
        print(prog.mlx_ptr)
        mlx.mlx_loop_exit(prog.mlx_ptr)
    timeend = time.perf_counter()
    time.sleep(max(0, 0.016 - (timeend - timestart)))  # Around ~60 FPS


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
    prog.quit = True


def run(config: dict[str, Any]) -> None:
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
        mlx_ptr = mlx_obj.mlx_init()
        if not mlx_ptr:
            raise RuntimeError(
                "Failed to initialize MiniLibX (mlx_init returned NULL). "
                "Ensure your DISPLAY environment variable is set."
            )
        win_ptr = mlx_obj.mlx_new_window(mlx_ptr, width, height, title)
        if not win_ptr:
            raise RuntimeError(
                "Failed to create MiniLibX window "
                "(mlx_new_window returned NULL)."
            )

        prog = Program(
            mlx_ptr,
            win_ptr,
            config,
            width,
            height,
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

    run(configs)


if __name__ == "__main__":
    main()
