from PIL.ImageDraw import ImageDraw
from gui.state import State
from PIL.Image import Image
class MazePanel:
    def draw(self, img: Image, state: State):
        canvas = ImageDraw(img)
        canvas.rectangle([(0, 0), img.size], 0xffffffff)
