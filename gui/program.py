from enum import Enum, auto
import gui.maze as gmaze
import gui.menu as gmenu
from typing import Any


class Event(Enum):
    NOTHING = auto()
    MAZE_NEW_SAME = auto()
    MAZE_NEW_RANDOM = auto()
    MAZE_SKIP = auto()


class Colors:
    """Class keeping color combinations for drawing a maze"""

    def __init__(self) -> None:
        self._maze_idx = 0
        self._emblem_idx = 0
        self._path_idx = 0
        self._maze_colors = [0xFF4F4F4F, 0xFF53CFE8, 0xFFE04EAA, 0xFFC9502C]
        self._emblem_colors = [0xFFFCE914, 0xFF12CE08, 0xFF6C29D1, 0xFF293AD1]
        self._path_colors = [0xFF52C2F9, 0xFF52F9DD, 0xFF28E034, 0xFF9D60F2]

    def maze_next(self) -> None:
        """Select next color for maze walls"""
        self._maze_idx = (self._maze_idx + 1) % len(self._maze_colors)

    def emblem_next(self) -> None:
        """Select next color for 42 emblem"""
        self._emblem_idx = (self._emblem_idx + 1) % len(self._emblem_colors)

    def path_next(self) -> None:
        """Select next color of the path"""
        self._path_idx = (self._path_idx + 1) % len(self._path_colors)

    @property
    def maze(self) -> int:
        """Color of the maze walls"""
        return self._maze_colors[self._maze_idx]

    @property
    def emblem(self) -> int:
        """Color of the 42 emblam"""
        return self._emblem_colors[self._emblem_idx]

    @property
    def path(self) -> int:
        """Color of the path"""
        return self._path_colors[self._path_idx]


class Program:
    """Class made to keep the state of the application"""

    def __init__(
        self,
        mlx_ptr: int,
        win_ptr: int,
        config: dict[str, Any],
        width: int,
        height: int,
        pause: bool = False
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
        self._width = width
        self._height = height
        self.active_menu = gmenu.MainMenuPanel()
        self.maze_panel = gmaze.MazeManager(config)
        self.pause = pause
        self.event: Event = Event.NOTHING
        self.quit = False
        self.show_path = True
        self._colors = Colors()

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
    def width(self) -> int:
        """Width of the window"""
        return self._width

    @property
    def height(self) -> int:
        """Height of the window"""
        return self._height

    @property
    def colors(self) -> Colors:
        """Color object of this program"""
        return self._colors
