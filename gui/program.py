from typing import Any
from gui.maze import MazePanel
from gui.menu import MainMenuPanel
from gui.state import State
from mlx import Mlx
from PIL import Image


class Program:
    def __init__(
        self,
        config: dict[str, Any],
        grid: list[list[int]],
        title: str = "A-Maze-Ing",
        width: int = 1440,
        height: int = 810,
    ) -> None:
        self._win_width = width
        self._win_height = height
        self._title = title
        self._config = config
        self._grid = grid

    def run(self) -> None:
        mlx_obj = None
        mlx_ptr = None
        win_ptr = None
        try:
            mlx_obj = Mlx()
            mlx_ptr = mlx_obj.mlx_init()
            if not mlx_ptr:
                return
            width = self._win_width if self._win_width else 1440
            height = self._win_height if self._win_height else 810
            win_ptr = mlx_obj.mlx_new_window(
                mlx_ptr, width, height, self._title
            )
            if not win_ptr:
                return

            main_menu = MainMenuPanel()
            maze_panel = MazePanel()

            state = State(
                mlx_ptr,
                win_ptr,
                width,
                height,
                main_menu,
                maze_panel,
                self._config,
                self._grid,
            )
            mlx_obj.mlx_key_hook(win_ptr, self._keys, state)
            mlx_obj.mlx_expose_hook(win_ptr, self._expose, state)
            mlx_obj.mlx_loop_hook(mlx_ptr, self._loop, state)
            mlx_obj.mlx_hook(win_ptr, 33, 0, self._close, state)
            mlx_obj.mlx_loop(mlx_ptr)
        finally:
            if mlx_obj and win_ptr:
                mlx_obj.mlx_destroy_window(mlx_ptr, win_ptr)
            if mlx_obj and mlx_ptr:
                mlx_obj.mlx_release(mlx_ptr)

    @staticmethod
    def _loop(state: State) -> None:
        menu_width = state.width // 4
        maze_border = 20
        maze_width = (state.width - menu_width) - maze_border * 2
        maze_height = state.height - maze_border * 2

        mlx = Mlx()

        # 1. Draw menu
        menu_ptr = mlx.mlx_new_image(state.mlx_ptr, menu_width, state.height)
        menu_data, _, _, _ = mlx.mlx_get_data_addr(menu_ptr)
        menu_img = Image.new(
            "RGBA", (menu_width, state.height), (30, 30, 30, 255)
        )
        state.active_menu.draw(menu_img)
        menu_data[:] = menu_img.tobytes()

        # 2. Draw maze using MazePanel
        maze_ptr = mlx.mlx_new_image(state.mlx_ptr, maze_width, maze_height)
        maze_data, _, _, _ = mlx.mlx_get_data_addr(maze_ptr)
        maze_img = Image.new(
            "RGBA", (maze_width, maze_height), (255, 255, 255, 255)
        )

        state.maze_panel.draw(maze_img, state)
        maze_data[:] = maze_img.tobytes()

        # 3. Present images to window
        mlx.mlx_clear_window(state.mlx_ptr, state.win_ptr)
        mlx.mlx_put_image_to_window(
            state.mlx_ptr, state.win_ptr, menu_ptr, state.width - menu_width, 0
        )
        mlx.mlx_put_image_to_window(
            state.mlx_ptr, state.win_ptr, maze_ptr, maze_border, maze_border
        )
        mlx.mlx_destroy_image(state.mlx_ptr, menu_ptr)
        mlx.mlx_destroy_image(state.mlx_ptr, maze_ptr)

        if state.quit:
            mlx.mlx_loop_exit(state.mlx_ptr)

    @staticmethod
    def _keys(key: int, state: State) -> None:
        if key == 65307:  # ESC
            state.quit = True
        state.active_menu.handle_keys(key, state)

    @staticmethod
    def _expose(state: State) -> None:
        pass

    @staticmethod
    def _close(state: State) -> None:
        Mlx().mlx_loop_exit(state.mlx_ptr)
