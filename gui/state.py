from typing import Any
import gui.menu as gmenu
import gui.maze as gmaze


class State:
    """Class made to keep the state of the application."""

    def __init__(
        self,
        mlx_ptr: int,
        win_ptr: int,
        width: int,
        height: int,
        menu: gmenu.MainMenuPanel,
        maze_panel: gmaze.MazePanel,
        config: dict[str, Any],
        grid: list[list[int]],
        pause: bool = False,
        skip: bool = False,
    ) -> None:
        self._mlx_ptr = mlx_ptr
        self._win_ptr = win_ptr
        self._width = width
        self._height = height
        self.active_menu = menu
        self.maze_panel = maze_panel
        self.config = config
        self.grid = grid
        self.pause = pause
        self.skip = skip
        self.quit = False

    @property
    def mlx_ptr(self) -> int:
        return self._mlx_ptr

    @property
    def win_ptr(self) -> int:
        return self._win_ptr

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height
