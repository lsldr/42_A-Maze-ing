import gui.program as gp
from PIL.Image import Image
from PIL.ImageDraw import ImageDraw
from mazegen.cell import Wall
from mazegen.util import Point


class MazeManager:
    """Class for managing the maze and drawing it on the screen."""

    def tick(self, prog: gp.Program) -> None:
        """Handles animations / generation ticks if active."""
        pass

    def draw(self, img: Image, prog: gp.Program) -> None:
        canvas = ImageDraw(img)
        width_cells = prog.config["width"]
        height_cells = prog.config["height"]
        entry = prog.config["entry"]
        exit_pos = prog.config["exit"]
        pattern = prog.config.get("pattern_cells", set())

        img_w, img_h = img.size
        cell_w = img_w / width_cells
        cell_h = img_h / height_cells

        wall_color = prog.colors.maze
        pattern_color = prog.colors.emblem

        # 1. Fill Entry, Exit, and 42 Pattern cells
        for x in range(width_cells):
            for y in range(height_cells):
                x0 = int(x * cell_w)
                y0 = int(y * cell_h)
                x1 = int((x + 1) * cell_w)
                y1 = int((y + 1) * cell_h)

                if (x, y) == entry:
                    canvas.rectangle(
                        [(x0, y0), (x1, y1)], fill="#A6E3A1"
                    )  # Green
                elif (x, y) == exit_pos:
                    canvas.rectangle(
                        [(x0, y0), (x1, y1)], fill="#F38BA8"
                    )  # Red
                elif (x, y) in pattern:
                    canvas.rectangle([(x0, y0), (x1, y1)], fill=pattern_color)

        # 2. Draw Walls based on cell bitmasks
        for x in range(width_cells):
            for y in range(height_cells):
                # prog.grid is list[list[Cell]] indexed by [x][y]
                cell = prog.grid[x][y]
                walls = cell.walls

                x0 = int(x * cell_w)
                y0 = int(y * cell_h)
                x1 = int((x + 1) * cell_w)
                y1 = int((y + 1) * cell_h)

                if Wall.NORTH in walls:
                    canvas.line([(x0, y0), (x1, y0)], fill=wall_color, width=2)
                if Wall.SOUTH in walls:
                    canvas.line([(x0, y1), (x1, y1)], fill=wall_color, width=2)
                if Wall.WEST in walls:
                    canvas.line([(x0, y0), (x0, y1)], fill=wall_color, width=2)
                if Wall.EAST in walls:
                    canvas.line([(x1, y0), (x1, y1)], fill=wall_color, width=2)
