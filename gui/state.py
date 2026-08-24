import gui.menu as gmenu


class State:
    """Class made to keep the state of the application"""
    def __init__(self,
                 mlx_ptr: int,
                 win_ptr: int,
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
        self.pause = pause
        self.skip = skip
        self.quit = False

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
