from gui.state import State
from mlx import Mlx


class Program:
    def __init__(self,
                 title: str = "Program",
                 width: int | None = None,
                 height: int | None = None) -> None:
        self._win_width = width
        self._win_height = height
        self._title = title

    def run(self) -> None:
        """Main function"""
        mlx_obj = Mlx()
        mlx_ptr: int | None = mlx_obj.mlx_init()
        if not mlx_ptr:
            return
        width = self._win_width if self._win_width else 1440
        height = self._win_height if self._win_height else 810
        win_ptr: int | None = mlx_obj.mlx_new_window(mlx_ptr,
                                                     width,
                                                     height,
                                                     "A-Maze-Ing")
        if not win_ptr:
            mlx_obj.mlx_release(mlx_ptr)
            return

        state = State(mlx_ptr, win_ptr, width, height)
        mlx_obj.mlx_key_hook(win_ptr, self._keys, state)
        mlx_obj.mlx_expose_hook(win_ptr, self._expose, state)
        mlx_obj.mlx_loop_hook(mlx_ptr, self._loop, state)
        mlx_obj.mlx_hook(win_ptr, 33, 0, self._close, state)
        mlx_obj.mlx_loop(mlx_ptr)

        mlx_obj.mlx_destroy_window(mlx_ptr, win_ptr)
        mlx_obj.mlx_release(mlx_ptr)

    @staticmethod
    def _loop(state: State) -> None:
        menu_width = state.width // 10
        mlx = Mlx()
        img_ptr = mlx.mlx_new_image(state.mlx_ptr, menu_width, state.height)
        img_data, bpp, lw, _ = mlx.mlx_get_data_addr(img_ptr)
        print(bpp, lw)
        for i in range(0, lw, 4):
            img_data[i:i + 4] = 0xffffffff.to_bytes(4, "little")
        mlx.mlx_put_image_to_window(state.mlx_ptr, state.win_ptr, img_ptr, 0,0)
        mlx.mlx_destroy_image(state.mlx_ptr, img_ptr)

    @staticmethod
    def _keys(key: int, state: State) -> None:
        print(key)

    @staticmethod
    def _expose(state: State) -> None:
        #print("Expose")
        pass

    @staticmethod
    def _close(state: State) -> None:
        Mlx().mlx_loop_exit(state.mlx_ptr)
