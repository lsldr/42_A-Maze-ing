import gui.program as gp
import PIL.Image
import PIL.ImageOps
from enum import Enum, auto
from mazegen import BFS_pathfinder, DFS_gen, Maze, Maze_Generator, Pathfinder
from mazegen.cell import Wall
from mazegen.util import Point
from PIL.Image import Image
from PIL.ImageDraw import ImageDraw
from random import Random
from typing import Any


class MazeManager:
    """Class for managing the maze and drawing it on the screen"""
    class State(Enum):
        MAZEGEN = auto()
        PATHFIND = auto()
        DONE = auto()

    def __init__(self, config: dict[str, Any]) -> None:
        width = config["width"]
        height = config["height"]
        entry = config["entry"]
        exit = config["exit"]
        gen = self._get_maze_gen(config)
        solv = self._get_path_solv(config)
        pattern = config["pattern_cells"]
        self._maze = Maze(Point(width, height), entry, exit, pattern)
        self._rand = Random()
        self._rand_init_state = self._rand.getstate()
        self._mazegen = gen(self._maze, self._rand, config["perfect"])
        self._pathfind = solv(self._maze)
        self._state = self.State.MAZEGEN
        self._first_maze = True  # only first maze will be written to file
        self._maze_gen_stack: list[Point] | None = None
        self._maze_gen_last: Point | None = None
        self._path_stack: list[Point] | None = None

    def _get_maze_gen(self, config: dict[str, Any]) -> type[Maze_Generator]:
        return DFS_gen

    def _get_path_solv(self, config: dict[str, Any]) -> type[Pathfinder]:
        return BFS_pathfinder

    def _output_first(self, file: str) -> None:
        if not self._first_maze:
            return
        self._mazegen.finish()
        self._pathfind.finish()
        try:
            with open(file, "w") as f:
                f.write(str(self._maze))
        except PermissionError:
            print("Error while writing to file: Access denied")
        self._first_maze = False

    def tick(self, prog: gp.Program) -> None:
        """Function to be called every loop of the program

        This function handles the maze generation

        Args:
            prog (Program): state object of the program
        """

        if prog.event in [gp.Event.MAZE_NEW_SAME, gp.Event.MAZE_NEW_RANDOM]:
            self._output_first(prog.config["output_file"])
            gen = self._get_maze_gen(prog.config)
            solv = self._get_path_solv(prog.config)
            perfect = prog.config["perfect"]
            pattern = prog.config["pattern_cells"]
            self._maze = Maze(self._maze.size,
                              self._maze.entry, self._maze.exit, pattern)
            if prog.event == gp.Event.MAZE_NEW_SAME:
                self._rand.setstate(self._rand_init_state)
            elif prog.event == gp.Event.MAZE_NEW_RANDOM:
                self._rand = Random()
                self._rand_init_state = self._rand.getstate()
            self._mazegen = gen(self._maze, self._rand, perfect)
            self._pathfind = solv(self._maze)
            self._maze_gen_last = None
            self._maze_gen_stack = None
            self._path_stack = None
            self._state = self.State.MAZEGEN
            prog.event = gp.Event.NOTHING

        if prog.event == gp.Event.MAZE_SKIP:
            if self._state == self.State.MAZEGEN:
                self._mazegen.finish()
                self._maze_gen_last = None
                self._maze_gen_stack = None
                self._state = self.State.PATHFIND
            elif self._state == self.State.PATHFIND:
                self._pathfind.finish()
                self._path_stack = None
                self._state = self.State.DONE
            prog.event = gp.Event.NOTHING

        if not prog.pause:
            match self._state:
                case self.State.MAZEGEN:
                    _, last, stack = self._mazegen.next()
                    self._maze_gen_last = last
                    self._maze_gen_stack = stack
                    if self._mazegen.is_ready():
                        self._mazegen.finish()
                        self._maze_gen_last = None
                        self._maze_gen_stack = None
                        self._state = self.State.PATHFIND
                case self.State.PATHFIND:
                    finished, self._path_stack = self._pathfind.next()
                    if finished:
                        self._path_stack = None
                        self._state = self.State.DONE
                case self.State.DONE:
                    self._output_first(prog.config["output_file"])

        if prog.quit:
            self._output_first(prog.config["output_file"])

    def draw(self, img: Image, prog: gp.Program) -> None:
        width_cells: int = prog.config["width"]
        height_cells: int = prog.config["height"]
        entry: Point = prog.config["entry"]
        exit_pos: Point = prog.config["exit"]
        pattern: set[tuple[int, int]] = prog.config.get("pattern_cells", set())

        tmp_img = PIL.Image.new("RGBA",
                                (width_cells * 32, height_cells * 32), "#DDD")
        canvas = ImageDraw(tmp_img)

        img_w, img_h = tmp_img.size
        cell_w = img_w / width_cells
        cell_h = img_h / height_cells

        wall_color = prog.colors.maze
        pattern_color = prog.colors.emblem

        # 1. Fill cells checked by pathfinder or mazegen
        for x in range(width_cells):
            for y in range(height_cells):
                x0 = int(x * cell_w)
                y0 = int(y * cell_h)
                x1 = int((x + 1) * cell_w)
                y1 = int((y + 1) * cell_h)

                if (self._maze_gen_stack and
                        Point(x, y) in self._maze_gen_stack):
                    canvas.rectangle(
                        [(x0, y0), (x1, y1)], fill="#BBB"
                        )  # darken
                if self._maze_gen_last == Point(x, y):
                    canvas.rectangle(
                        [(x0, y0), (x1, y1)], fill="#AAA"
                    )  # darken
                if self._path_stack and Point(x, y) in self._path_stack:
                    canvas.rectangle(
                        [(x0, y0), (x1, y1)], fill="#AAA"
                    )  # darken

        # 2. Draw path when ready
        if self._maze.path and prog.show_path:
            off_w = cell_w / 2
            off_h = cell_h / 2
            path = [(x * cell_w + off_w, y * cell_h + off_h) for
                    x, y in self._maze.path]
            canvas.line(path,
                        prog.colors.path, round(min(cell_h, cell_w) // 2),
                        "curve")

        # 3. Fill Entry, Exit, and 42 Pattern cells
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

        # 4. Draw Walls based on cell bitmasks
        for x in range(width_cells):
            for y in range(height_cells):
                # prog.grid is list[list[Cell]] indexed by [x][y]
                cell = self._maze.get_cell(Point(x, y))
                walls = cell.walls

                x0 = int(x * cell_w)
                y0 = int(y * cell_h)
                x1 = int((x + 1) * cell_w)
                y1 = int((y + 1) * cell_h)

                if cell.visited and Wall.NORTH in walls:
                    canvas.line([(x0, y0), (x1, y0)], fill=wall_color, width=2)
                if cell.visited and Wall.SOUTH in walls:
                    canvas.line([(x0, y1), (x1, y1)], fill=wall_color, width=2)
                if cell.visited and Wall.WEST in walls:
                    canvas.line([(x0, y0), (x0, y1)], fill=wall_color, width=2)
                if cell.visited and Wall.EAST in walls:
                    canvas.line([(x1, y0), (x1, y1)], fill=wall_color, width=2)

        tmp_img = PIL.ImageOps.contain(tmp_img, img.size)
        offset = ((img.size[0] - tmp_img.size[0]) // 2,
                  (img.size[1] - tmp_img.size[1]) // 2)
        img.paste(tmp_img, offset)
