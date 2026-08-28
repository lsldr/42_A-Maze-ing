from pathlib import Path
from random import Random
from subprocess import run
import sys

from mazegen import IRK_Gen, DFSGen, WilsonsGen, Maze, Point

sizes = [(3, 3), (5, 7), (10, 10), (20, 15)]

if len(sys.argv) != 2:
    print("Provide an argument with the mazegen class name to test!")
    print("Accepted class names: [IRK_Gen, DFSGen, WilsonsGen]")
    sys.exit(1)

raw_arg_name = sys.argv[1]

if raw_arg_name not in ["IRK_Gen", "DFSGen", "WilsonsGen"]:
    print("Accepted class names: [IRK_Gen, DFSGen, WilsonsGen]")
    sys.exit(1)

for width, height in sizes:
    for perfect in (True, False):
        path = Path(f"/tmp/irk_{width}x{height}_{perfect}.txt")

        maze = Maze(
            Point(width, height),
            Point(0, 0),
            Point(width - 1, height - 1),
        )
        if raw_arg_name == "IRK_Gen":
            generator = IRK_Gen(maze, Random(42), perfect)
        elif raw_arg_name == "DFSGen":
            generator = DFSGen(maze, Random(42), perfect)
        elif raw_arg_name == "WilsonsGen":
            generator = WilsonsGen(maze, Random(42), perfect)
        generator.finish()
        path.write_text(str(maze))

        print(f"=== {width}x{height}, PERFECT={perfect} ===")
        result = run(
            [
                "uv",
                "run",
                "python",
                "maze_analyzer.py",
                str(path),
                "--min-loops",
                "0",
                "--max-dead-ends",
                str(width * height),
            ],
            capture_output=True,
            text=True,
        )
        print(result.stdout)
