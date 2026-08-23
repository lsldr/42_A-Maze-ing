import gui.menu as gmenu


class State:
    def __init__(self,
                 mlx_ptr: int,
                 win_ptr: int,
                 width: int,
                 height: int,
                 menu: gmenu.MainMenuPanel,
                 pause: bool = True,
                 skip: bool = False
                 ) -> None:
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
