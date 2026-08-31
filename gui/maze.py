import gui.program as gp
import PIL.Image
import PIL.ImageOps
import sys
from enum import Enum, auto
from mazegen import (
    AStarPathfinder,
    BFSPathfinder,
    DFSGen,
    IRK_Gen,
    Maze,
    MazeGenerator,
    Pathfinder,
    WilsonsGen,
)
from mazegen.cell import Wall
from mazegen.util import Point
from PIL.Image import Image
from PIL.ImageDraw import ImageDraw
from random import Random
from typing import Any


class MazeManager:
    """Manage maze generation, pathfinding state, and screen rendering.

    Attributes:
        State (Enum): Enum defining the lifecycle states of maze processing.
    """

    class State(Enum):
        MAZEGEN = auto()
        PATHFIND = auto()
        DONE = auto()

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize the MazeManager.

        Args:
            config (dict[str, Any]): Parsed application configuration
                dictionary.
        """
        width = config["width"]
        height = config["height"]
        entry = config["entry"]
        exit = config["exit"]
        self._walls_vis = False
        seed = config["seed"]
        gen = self._get_maze_gen(config)
        solv = self._get_path_solv(config)
        pattern = config["pattern_cells"]
        self._maze = Maze(Point(width, height), entry, exit, pattern)
        self._rand = Random(seed)
        self._rand_init_state = self._rand.getstate()
        self._mazegen = gen(self._maze, self._rand, config["perfect"])
        self._pathfind = solv(self._maze)
        self._state = self.State.MAZEGEN
        self._first_maze = True  # only first maze will be written to file
        self._maze_gen_stack: list[Point] | None = None
        self._maze_gen_last: Point | None = None
        self._path_stack: list[Point] | None = None

    def _get_maze_gen(self, config: dict[str, Any]) -> type[MazeGenerator]:
        """Select the maze generator class based on configuration.

        Args:
            config (dict[str, Any]): Configuration dictionary.

        Returns:
            type[MazeGenerator]: Selected MazeGenerator subclass.
        """
        algo = config["mazegen"]
        self._walls_vis = False
        match algo:
            case "dfs":
                return DFSGen
            case "wilson":
                return WilsonsGen
            case "irk":
                self._walls_vis = True
                return IRK_Gen
        return DFSGen

    def _get_path_solv(self, config: dict[str, Any]) -> type[Pathfinder]:
        """Select the pathfinder class based on configuration.

        Args:
            config (dict[str, Any]): Configuration dictionary.

        Returns:
            type[Pathfinder]: Selected Pathfinder subclass.
        """
        algo = config.get("pathfinding", "bfs")
        match algo:
            case "bfs":
                return BFSPathfinder
            case "astar" | "a_star":
                return AStarPathfinder
        return BFSPathfinder

    def _toggle_pathfinding(self, config: dict[str, Any]) -> type[Pathfinder]:
        """Switch to the alternate solver for the current maze."""
        current = config.get("pathfinding", "bfs")
        next_algo = "astar" if current == "bfs" else "bfs"
        config["pathfinding"] = next_algo
        return self._get_path_solv(config)

    def _output_first(self, file: str) -> None:
        """Write the first generated maze and path to an output file.

        Args:
            file (str): Path of the destination output file.
        """
        if not self._first_maze:
            return
        self._mazegen.finish()
        self._pathfind.finish()
        try:
            with open(file, "w") as f:
                f.write(str(self._maze))
        except PermissionError:
            print(
                "Error while writing to file: Access denied", file=sys.stderr
            )
        self._first_maze = False

    def tick(self, prog: gp.Program) -> None:
        """Advance maze generation or pathfinding state by one tick.

        Args:
            prog (gp.Program): Main program state object.
        """
        if prog.event in [gp.Event.MAZE_NEW_SAME, gp.Event.MAZE_NEW_RANDOM]:
            self._output_first(prog.config["output_file"])
            gen = self._get_maze_gen(prog.config)
            solv = self._get_path_solv(prog.config)
            perfect = prog.config["perfect"]
            pattern = prog.config["pattern_cells"]
            self._maze = Maze(
                self._maze.size, self._maze.entry, self._maze.exit, pattern
            )
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

        if prog.event == gp.Event.PATHFIND_ALTERNATE:
            if self._state != self.State.MAZEGEN:
                solver_cls = self._toggle_pathfinding(prog.config)
                self._pathfind = solver_cls(self._maze)
                self._path_stack = None
                self._state = self.State.PATHFIND
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
        """Draw the current maze, active cells, and path onto an image canvas.

        Args:
            img (Image): Pillow RGBA image canvas to draw on.
            prog (gp.Program): Main program state object.
        """
        width_cells: int = prog.config["width"]
        height_cells: int = prog.config["height"]
        entry: Point = prog.config["entry"]
        exit_pos: Point = prog.config["exit"]
        pattern: set[tuple[int, int]] = prog.config.get("pattern_cells", set())

        tmp_img = PIL.Image.new(
            "RGBA", (width_cells * 16, height_cells * 16), "#DDD"
        )
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

                if (
                    self._maze_gen_stack
                    and Point(x, y) in self._maze_gen_stack
                ):
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
            path = [
                (x * cell_w + off_w, y * cell_h + off_h)
                for x, y in self._maze.path
            ]
            canvas.line(
                path,
                prog.colors.path,
                round(min(cell_h, cell_w) // 2),
                "curve",
            )

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
                if (self._walls_vis or cell.visited) and (x, y) not in pattern:
                    if Wall.NORTH in walls:
                        canvas.line(
                            [(x0, y0), (x1, y0)], fill=wall_color, width=2
                        )
                    if Wall.SOUTH in walls:
                        canvas.line(
                            [(x0, y1), (x1, y1)], fill=wall_color, width=2
                        )
                    if Wall.WEST in walls:
                        canvas.line(
                            [(x0, y0), (x0, y1)], fill=wall_color, width=2
                        )
                    if Wall.EAST in walls:
                        canvas.line(
                            [(x1, y0), (x1, y1)], fill=wall_color, width=2
                        )

        tmp_img = PIL.ImageOps.contain(tmp_img, img.size)
        offset = (
            (img.size[0] - tmp_img.size[0]) // 2,
            (img.size[1] - tmp_img.size[1]) // 2,
        )
        img.paste(tmp_img, offset)
