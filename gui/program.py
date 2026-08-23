from gui.menu import MainMenuPanel
from gui.state import State
from mlx import Mlx
from PIL import Image


class Program:
    """Base class for a-maze-ing program

    This class handels creation of window as well as callbacks for application
    loop
    """
    def __init__(self,
                 title: str = "Program",
                 width: int = 1440,
                 height: int = 810) -> None:
        """Base class for a-maze-ing program

        Args:
            title (str): Title of a program
                (will be seen on top of the application)
            width (int): Width of the window
            height (int): Height of the window
        """
        self._win_width = width
        self._win_height = height
        self._title = title

    def run(self) -> None:
        """Main function of this class

        Creates window and start main application loop
        Will only return when application stop
        """
        try:
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
                return

            main_menu = MainMenuPanel()

            state = State(mlx_ptr, win_ptr, width, height, main_menu)
            mlx_obj.mlx_key_hook(win_ptr, self._keys, state)
            mlx_obj.mlx_expose_hook(win_ptr, self._expose, state)
            mlx_obj.mlx_loop_hook(mlx_ptr, self._loop, state)
            mlx_obj.mlx_hook(win_ptr, 33, 0, self._close, state)
            mlx_obj.mlx_loop(mlx_ptr)
        finally:
            if win_ptr:
                mlx_obj.mlx_destroy_window(mlx_ptr, win_ptr)
            if mlx_ptr:
                mlx_obj.mlx_release(mlx_ptr)

    @staticmethod
    def _loop(state: State) -> None:
        """Callback for main application loop

        Args:
            state (State): object kepping the state of application
        """
        menu_width = state.width // 4
        maze_border = 20
        maze_width = ((state.width - menu_width) - maze_border * 2)
        maze_height = state.height - maze_border * 2

        mlx = Mlx()

        # Draw menu
        menu_ptr = mlx.mlx_new_image(state.mlx_ptr, menu_width, state.height)
        menu_data, _, _, _ = mlx.mlx_get_data_addr(menu_ptr)
        menu = Image.new("RGBA", (menu_width, state.height))

        state.active_menu.draw(menu)

        menu_data[:] = menu.tobytes()

        # draw maze
        maze_ptr = mlx.mlx_new_image(state.mlx_ptr, maze_width, maze_height)
        maze_data, _, _, _ = mlx.mlx_get_data_addr(maze_ptr)
        maze = Image.new("RGBA", (maze_width, maze_height), 0xffffffff)

        maze_data[:] = maze.tobytes()
        mlx.mlx_clear_window(state.mlx_ptr, state.win_ptr)
        mlx.mlx_put_image_to_window(state.mlx_ptr,
                                    state.win_ptr,
                                    menu_ptr,
                                    state.width - menu_width,
                                    0)
        mlx.mlx_put_image_to_window(state.mlx_ptr,
                                    state.win_ptr,
                                    maze_ptr,
                                    maze_border,
                                    maze_border)
        mlx.mlx_destroy_image(state.mlx_ptr, menu_ptr)
        mlx.mlx_destroy_image(state.mlx_ptr, maze_ptr)
        if state.quit:
            mlx.mlx_loop_exit(state.mlx_ptr)

    @staticmethod
    def _keys(key: int, state: State) -> None:
        """Callback for handling key input
        Only released key is send

        Args:
            key (int): keycode of pressed key
            state (State): object kepping the state of application
        """
        if key == 65307:
            state.quit = True
        state.active_menu.handle_keys(key, state)

    @staticmethod
    def _expose(state: State) -> None:
        """Callback for expose event

        Expose is called when X11 request repainting of the window

        Args:
            state (State): object kepping the state of application
        """
        #print("Expose")

    @staticmethod
    def _close(state: State) -> None:
        """Callback for when the close button of the window was pressed

        Args:
            state (State): object kepping the state of application
        """
        Mlx().mlx_loop_exit(state.mlx_ptr)
