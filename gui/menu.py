from gui import program
from PIL import Image
from PIL import ImageDraw


class MainMenuPanel:
    """Main menu of application"""

    def __init__(self) -> None:
        """Function used to draw the menu on screen

        Args:
            img (Image): pillow Image object used to draw menu on screen
            state (State): state object of the application
        """
        super().__init__()
        self._font_size = 20
        self._menu_list = [
            "Space: Start/Stop",
            "p: skip animation",
            "x: change maze color",
            "c: change 42 color",
            "v: change path color",
            "d: show/hide path",
            "n: new maze from random seed",
            "m: new maze from seed",
            "q: quit"
        ]

    def handle_keys(self, key: int, prog: program.Program) -> None:
        """Handles the keys for the menu

        Args:
            key (int): keycode of keyboard
            state (State): state object of the program
        """
        match key:
            case 32: # space start/pause
                prog.pause = not prog.pause
            case 99: # c change 42 color
                prog.colors.emblem_next()
            case 100: # d show/hide path
                prog.show_path = not prog.show_path
            case 109: # m new maze same seed
                prog.event = program.Event.MAZE_NEW_SAME
            case 110: # n new maze new seed
                prog.event = program.Event.MAZE_NEW_RANDOM
            case 112: # p skip maze anim
                prog.event = program.Event.MAZE_SKIP
            case 113:
                prog.quit = True
            case 118: # v change path color
                prog.colors.path_next()
            case 120: # x change maze color
                prog.colors.maze_next()

    def draw(self, img: Image.Image) -> None:
        """Function used to draw the menu on screen."""
        canvas = ImageDraw.Draw(img)

        if self._menu_list:
            for i, el in enumerate(self._menu_list):
                canvas.text(
                    (10, 20 * (i + 1) + self._font_size * i),
                    el,
                    fill="white",  # Make text visible
                    font_size=self._font_size,
                )
