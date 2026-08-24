import gui.menu as gmenu
import gui.maze as gmaze
from typing import Any


class Colors:
    """Class keeping color combinations for drawing a maze"""
    def __init__(self) -> None:
        self._maze_idx = 0
        self._emblem_idx = 0
        self._path_idx = 0
        self._maze_colors = [0Xff4F4F4F,
                                        0XFF53CFE8,
                                        0XFFE04EAA,
                                        0XFFC9502C
                                       ]
        self._emblem_colors = [0Xfffce914,
                                          0Xff12CE08,
                                          0Xff6C29D1,
                                          0Xff293AD1
                                         ]
        self._path_colors = [0Xff52C2F9,
                                        0XFF52F9DD,
                                        0XFF28E034,
                                        0XFF9D60F2
                                       ]

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
    def __init__(self,
                 mlx_ptr: int,
                 win_ptr: int,
                 config: dict[str, Any],
                 width: int,
                 height: int,
                 menu: gmenu.MainMenuPanel,
                 pause: bool = False,
                 skip: bool = False
                 ) -> None:
        """Class made to keep the state of the application

        Args:
            mlx_ptr (int): pointer to the mlx systems
            win_ptr (int): pointer to the main window of the application
            width (int): width of the window in pixels
            height (int): height of the window in pixels
            menu (MainMenuPanel): menu class used by this application
            pause (bool): if animation should be paused
            skip (bool): if True skip animation and show finished result
        """
        self._mlx_ptr = mlx_ptr
        self._win_ptr = win_ptr
        self._width = width
        self._height = height
        self.active_menu = menu
        self.maze = gmaze.MazeManager()
        self.pause = pause
        self.skip = skip
        self.quit = False
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
