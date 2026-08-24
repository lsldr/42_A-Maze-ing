from gui.program import Program
from PIL.Image import Image
from PIL.ImageDraw import ImageDraw


class MazePanel:
    """Class for managing the maze and drawing it on the screen"""
    def loop(self, img: Image, prog: Program) -> None:
        """Function to be called every loop of the program

        This function handles the maze generation and
        drawing it on to the image canvas

        Args:
            img (Image): the image on which to draw the maze to
            state (State): state object of the program
        """
        canvas = ImageDraw(img)
        canvas.rectangle([(0, 0), img.size], 0xffffffff)
