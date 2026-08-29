import gui.maze as gmaze
import gui.menu as gmenu
from enum import Enum, auto
from typing import Any


class Event(Enum):
    NOTHING = auto()
    MAZE_NEW_SAME = auto()
    MAZE_NEW_RANDOM = auto()
    MAZE_SKIP = auto()
    PATHFIND_ALTERNATE = auto()


class Colors:
    """Manages color palettes for drawing maze components."""

    def __init__(self) -> None:
        """Initialize color palette indices and hex values."""
        self._maze_idx = 0
        self._emblem_idx = 0
        self._path_idx = 0
        self._maze_colors = [0xFF4F4F4F, 0xFF53CFE8, 0xFFE04EAA, 0xFFC9502C]
        self._emblem_colors = [0xFFFCE914, 0xFF12CE08, 0xFF6C29D1, 0xFF293AD1]
        self._path_colors = [0xFF52C2F9, 0xFF52F9DD, 0xFF28E034, 0xFF9D60F2]

    def maze_next(self) -> None:
        """Cycle to the next wall color."""
        self._maze_idx = (self._maze_idx + 1) % len(self._maze_colors)

    def emblem_next(self) -> None:
        """Cycle to the next emblem color."""
        self._emblem_idx = (self._emblem_idx + 1) % len(self._emblem_colors)

    def path_next(self) -> None:
        """Cycle to the next solution path color."""
        self._path_idx = (self._path_idx + 1) % len(self._path_colors)

    @property
    def maze(self) -> int:
        """int: Active color value for maze walls."""
        return self._maze_colors[self._maze_idx]

    @property
    def emblem(self) -> int:
        """int: Active color value for the 42 emblem."""
        return self._emblem_colors[self._emblem_idx]

    @property
    def path(self) -> int:
        """int: Active color value for the solution path."""
        return self._path_colors[self._path_idx]


class Program:
    """Maintains the runtime state of the application.

    Attributes:
        active_menu (gmenu.MainMenuPanel): Active interactive menu.
        maze_panel (gmaze.MazeManager): Manager handling maze logic
            and drawing.
        pause (bool): Flag indicating if animation is paused.
        event (Event): Current pending application event.
        quit (bool): Flag indicating if program should exit.
        show_path (bool): Flag controlling visibility of the solution path.
    """

    def __init__(
        self,
        mlx_ptr: int,
        win_ptr: int,
        config: dict[str, Any],
        width: int,
        height: int,
        pause: bool = False,
    ) -> None:
        """Initialize application state.

        Args:
            mlx_ptr (int): Pointer to the MiniLibX system instance.
            win_ptr (int): Pointer to the main application window.
            config (dict[str, Any]): Parsed maze configuration dictionary.
            width (int): Width of the window in pixels.
            height (int): Height of the window in pixels.
            pause (bool, optional): Initial pause state. Defaults to False.
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
        """int: Pointer to the MiniLibX system instance."""
        return self._mlx_ptr

    @property
    def win_ptr(self) -> int:
        """int: Pointer to the application window."""
        return self._win_ptr

    @property
    def config(self) -> dict[str, Any]:
        """dict[str, Any]: Parsed configuration dictionary."""
        return self._config

    @property
    def width(self) -> int:
        """int: Width of the window in pixels."""
        return self._width

    @property
    def height(self) -> int:
        """int: Height of the window in pixels."""
        return self._height

    @property
    def colors(self) -> Colors:
        """Colors: Color manager for application rendering."""
        return self._colors
