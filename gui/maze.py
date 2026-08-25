import gui.program as gp
from PIL.Image import Image
from PIL.ImageDraw import ImageDraw


class MazeManager:
    """Class for managing the maze and drawing it on the screen"""

    def tick(self, prog: gp.Program) -> None:
        """Function to be called every loop of the program

        This function handles the maze generation

        Args:
            prog (Program): state object of the program
        """

    def draw(self, img: Image, prog: gp.Program) -> None:
        """Function to be called every loop of the program

        This function handles drawing the maze on screen

        Args:
            img (Image): the image on which to draw the maze to
            prog (Program): state object of the program
        """
        canvas = ImageDraw(img)
        xhalf = img.size[0] // 2
        yhalf = img.size[1] // 2
        # canvas.rectangle([(0, 0), img.size], 0xffffffff)
        canvas.rectangle([(0, 0), (xhalf, yhalf)], prog.colors.maze)
        canvas.rectangle(
            [(xhalf, 0), (img.size[0], yhalf)], prog.colors.emblem
        )
        canvas.rectangle([(0, yhalf), (xhalf, img.size[1])], prog.colors.path)
