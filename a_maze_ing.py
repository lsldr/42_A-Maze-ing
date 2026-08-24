from typing import Any
import sys
from gui.menu import MainMenuPanel
from gui.program import Program
from mazegen.input_parser import ConfigError, parse_config
from mlx import Mlx
from PIL import Image


def loop_callback(prog: Program) -> None:
    """Callback for main application loop

    Args:
        state (State): object kepping the state of application
    """
    menu_width = prog.width // 4
    maze_border = 20
    maze_width = (prog.width - menu_width) - maze_border * 2
    maze_height = prog.height - maze_border * 2

    mlx = Mlx()

    # Draw menu
    menu_ptr = mlx.mlx_new_image(prog.mlx_ptr, menu_width, prog.height)
    menu_data, _, _, _ = mlx.mlx_get_data_addr(menu_ptr)
    menu = Image.new("RGBA", (menu_width, prog.height))

    prog.active_menu.draw(menu)

    menu_data[:] = menu.tobytes()

    # draw maze
    maze_ptr = mlx.mlx_new_image(prog.mlx_ptr, maze_width, maze_height)
    maze_data, _, _, _ = mlx.mlx_get_data_addr(maze_ptr)
    maze = Image.new("RGBA", (maze_width, maze_height), 0xFFFFFFFF)

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


def keys_callback(key: int, prog: Program) -> None:
    """Callback for handling key input
    Only released key is send

    Args:
        key (int): keycode of pressed key
        state (State): object kepping the state of application
    """
    if key == 65307:
        prog.quit = True
    prog.active_menu.handle_keys(key, prog)


def expose_callback(prog: Program) -> None:
    """Callback for expose event

    Expose is called when X11 request repainting of the window

    Args:
        state (State): object kepping the state of application
    """
    # print("Expose")


def close_callback(prog: Program) -> None:
    """Callback for when the close button of the window was pressed

    Args:
        state (State): object kepping the state of application
    """
    Mlx().mlx_loop_exit(prog.mlx_ptr)


def run(config: dict[str, Any]) -> None:
    """Main function of this class

    Creates window and start main application loop
    Will only return when application stop
    """
    width = 1440
    height = 810
    title = "A-Maze-Ing"
    try:
        mlx_obj = Mlx()
        mlx_ptr: int | None = mlx_obj.mlx_init()
        if not mlx_ptr:
            return
        win_ptr: int | None = mlx_obj.mlx_new_window(
            mlx_ptr, width, height, title
        )
        if not win_ptr:
            return

        main_menu = MainMenuPanel()

        prog = Program(mlx_ptr, win_ptr, config, width, height, main_menu)
        mlx_obj.mlx_key_hook(win_ptr, keys_callback, prog)
        mlx_obj.mlx_expose_hook(win_ptr, expose_callback, prog)
        mlx_obj.mlx_loop_hook(mlx_ptr, loop_callback, prog)
        mlx_obj.mlx_hook(win_ptr, 33, 0, close_callback, prog)
        mlx_obj.mlx_loop(mlx_ptr)
    finally:
        if win_ptr:
            mlx_obj.mlx_destroy_window(mlx_ptr, win_ptr)
        if mlx_ptr:
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
        config_dict = parse_config(sys.argv[1].strip())
        print(config_dict)
        run(config_dict)
    except (FileNotFoundError, ConfigError) as e:
        print(f"Error parsing configs with the provided filename:\n{e}")


if __name__ == "__main__":
    main()
