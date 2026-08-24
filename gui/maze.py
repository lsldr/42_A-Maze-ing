from PIL import Image, ImageDraw
import gui.state as st
from mazegen.maze_generator import Wall


class MazePanel:
    """Class for managing the maze and drawing it on the screen."""

    def draw(self, img: Image.Image, state: "st.State") -> None:
        """Draw the maze grid, walls, pattern, and entry/exit onto the canvas."""
        if not state.grid:
            return

        draw = ImageDraw.Draw(img)
        width_px, height_px = img.size
        cols = state.config["width"]
        rows = state.config["height"]

        # Calculate cell size and offsets to center the maze in the viewport
        cell_size = min(width_px // cols, height_px // rows)
        offset_x = (width_px - (cols * cell_size)) // 2
        offset_y = (height_px - (rows * cell_size)) // 2

        # Optional: Background fill
        draw.rectangle(
            [(0, 0), (width_px, height_px)], fill=(240, 240, 240, 255)
        )

        pattern_cells = state.config.get("pattern_cells", set())
        entry = state.config.get("entry")
        exit_pos = state.config.get("exit")

        wall_color = (40, 40, 40, 255)
        wall_thickness = max(2, cell_size // 10)

        for y in range(rows):
            for x in range(cols):
                c_x1 = offset_x + x * cell_size
                c_y1 = offset_y + y * cell_size
                c_x2 = c_x1 + cell_size
                c_y2 = c_y1 + cell_size

                # Draw cell highlights (Pattern 42, Entry, Exit)
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
                cell = state.grid[y][x]
                if cell & Wall.NORTH:
                    draw.line(
                        [(c_x1, c_y1), (c_x2, c_y1)],
                        fill=wall_color,
                        width=wall_thickness,
                    )
                if cell & Wall.SOUTH:
                    draw.line(
                        [(c_x1, c_y2), (c_x2, c_y2)],
                        fill=wall_color,
                        width=wall_thickness,
                    )
                if cell & Wall.WEST:
                    draw.line(
                        [(c_x1, c_y1), (c_x1, c_y2)],
                        fill=wall_color,
                        width=wall_thickness,
                    )
                if cell & Wall.EAST:
                    draw.line(
                        [(c_x2, c_y1), (c_x2, c_y2)],
                        fill=wall_color,
                        width=wall_thickness,
                    )
