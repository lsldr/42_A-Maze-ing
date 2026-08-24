from typing import Any
import gui.menu as gmenu
import gui.maze as gmaze


class Program:
    """Class made to keep the state of the application"""

    def __init__(
        self,
        mlx_ptr: int,
        win_ptr: int,
        config: dict[str, Any],
        grid: list[list[int]],
        width: int,
        height: int,
        menu: gmenu.MainMenuPanel,
        maze_panel: gmaze.MazePanel,
        pause: bool = False,
        skip: bool = False,
    ) -> None:
        """Class made to keep the state of the application

        Args:
            mlx_ptr (int): pointer to the mlx systems
            win_ptr (int): pointer to the main window of the application
            config (dict[str, Any]): parsed maze configuration dictionary
            grid (list[list[int]]): 2D grid representing maze wall bitmasks
            width (int): width of the window in pixels
            height (int): height of the window in pixels
            menu (MainMenuPanel): menu class used by this application
            maze_panel (MazePanel): panel responsible for drawing the maze
            pause (bool): if animation should be paused
            skip (bool): if True skip animation and show finished result
        """
        self._mlx_ptr = mlx_ptr
        self._win_ptr = win_ptr
        self._config = config
        self._grid = grid
        self._width = width
        self._height = height
        self._active_maze = maze_panel
        self._active_menu = menu
        self._pause = pause
        self._skip = skip
        self._quit = False

    @property
    def mlx_ptr(self) -> int:
        """Pointer to the mlx systems"""
        return self._mlx_ptr

    @property
    def win_ptr(self) -> int:
        """Pointer to the window"""
        return self._win_ptr

    @property
    def config(self) -> dict[str, Any]:
        """Parsed maze configuration dictionary"""
        return self._config

    @property
    def grid(self) -> list[list[int]]:
        """2D grid of maze cell bitmasks"""
        return self._grid

    @grid.setter
    def grid(self, value: list[list[int]]) -> None:
        self._grid = value

    @property
    def width(self) -> int:
        """Width of the window"""
        return self._width

    @property
    def height(self) -> int:
        """Height of the window"""
        return self._height

    @property
    def active_maze(self) -> gmaze.MazePanel:
        """Active maze drawing panel"""
        return self._active_maze

    @property
    def active_menu(self) -> gmenu.MainMenuPanel:
        """Active menu panel"""
        return self._active_menu

    @property
    def pause(self) -> bool:
        """Whether animation is paused"""
        return self._pause

    @pause.setter
    def pause(self, value: bool) -> None:
        self._pause = value

    @property
    def skip(self) -> bool:
        """Whether animation is skipped"""
        return self._skip

    @skip.setter
    def skip(self, value: bool) -> None:
        self._skip = value

    @property
    def quit(self) -> bool:
        """Whether application requested to quit"""
        return self._quit

    @quit.setter
    def quit(self, value: bool) -> None:
        self._quit = value
