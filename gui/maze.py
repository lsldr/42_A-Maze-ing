from PIL import Image, ImageDraw
import gui.program as program
from mazegen.maze_generator import Wall


class MazePanel:
    """Class for managing the maze and drawing it on the screen"""

    def draw(self, img: Image.Image, prog: "program") -> None:
        if not prog.grid:
            return
        draw = ImageDraw.Draw(img)
        width_px, height_px = img.size
        cols = prog.config["width"]
        rows = prog.config["height"]
        # Calculate cell size so maze fits inside the image viewport
        cell_size = min(width_px // cols, height_px // rows)
        offset_x = (width_px - (cols * cell_size)) // 2
        offset_y = (height_px - (rows * cell_size)) // 2
        # Background
        draw.rectangle(
            [(0, 0), (width_px, height_px)], fill=(240, 240, 240, 255)
        )
        entry = prog.config.get("entry")
        exit_pos = prog.config.get("exit")
        pattern_cells = prog.config.get("pattern_cells", set())
        wall_color = (30, 30, 30, 255)
        wall_width = max(2, cell_size // 10)
        for y in range(rows):
            for x in range(cols):
                c_x1 = offset_x + x * cell_size
                c_y1 = offset_y + y * cell_size
                c_x2 = c_x1 + cell_size
                c_y2 = c_y1 + cell_size
                # Cell color fills: Entry, Exit, 42 Pattern
                if (x, y) == entry:
                    draw.rectangle(
                        [(c_x1, c_y1), (c_x2, c_y2)], fill=(100, 220, 100, 255)
                    )
                elif (x, y) == exit_pos:
                    draw.rectangle(
                        [(c_x1, c_y1), (c_x2, c_y2)], fill=(220, 100, 100, 255)
                    )
                elif (x, y) in pattern_cells:
                    draw.rectangle(
                        [(c_x1, c_y1), (c_x2, c_y2)], fill=(250, 210, 40, 255)
                    )
                # Draw walls using bitmasks
                cell = prog.grid[y][x]
                if cell & Wall.NORTH:
                    draw.line(
                        [(c_x1, c_y1), (c_x2, c_y1)],
                        fill=wall_color,
                        width=wall_width,
                    )
                if cell & Wall.SOUTH:
                    draw.line(
                        [(c_x1, c_y2), (c_x2, c_y2)],
                        fill=wall_color,
                        width=wall_width,
                    )
                if cell & Wall.WEST:
                    draw.line(
                        [(c_x1, c_y1), (c_x1, c_y2)],
                        fill=wall_color,
                        width=wall_width,
                    )
                if cell & Wall.EAST:
                    draw.line(
                        [(c_x2, c_y1), (c_x2, c_y2)],
                        fill=wall_color,
                        width=wall_width,
                    )
