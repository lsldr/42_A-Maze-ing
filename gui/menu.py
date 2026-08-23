import gui.state as st
from PIL.Image import Image
from PIL.ImageDraw import ImageDraw


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
            "c: change maze color",
            "v: change 42 color",
            "n: new maze from random seed",
            "m: new maze from seed",
            "q: quit"
        ]

    def handle_keys(self, key: int, state: st.State) -> None:
        match key:
            case 32: # space start/pause
                state.pause = not state.pause
            case 112: # p skip maze anim
                state.skip = True
            case 99: # c change maze color
                print("maze color") #TODO: change maze color
            case 118: # v change 42 color
                print("42 color") #TODO: change 42 color
            case 110: # n new maze new seed
                print("new rand") #TODO: seed to random
            case 109: # m new maze same seed
                print("old rand") #TODO: reload maze
            case 113:
                state.quit = True

    def draw(self, img: Image) -> None:
        """Function used to draw the menu on screen

           Args:
               img (Image): pillow Image object used to draw menu on screen
               state (State): state object of the application
        """
        canvas = ImageDraw(img)

        if self._menu_list:
            for i, el in enumerate(self._menu_list):
                canvas.text((0, 20 * (i + 1) + self._font_size * i),
                            el,
                            font_size = self._font_size)
