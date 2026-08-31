from pathlib import Path
from random import Random
from subprocess import run
import sys

from mazegen import IRK_Gen, DFSGen, WilsonsGen, Maze, Point, MazeGenerator

ROOT = Path(__file__).resolve().parent.parent
ANALYZER = ROOT / "test_scripts" / "maze_analyzer.py"
SIZES = [(3, 3), (5, 7), (10, 10), (20, 15)]

if len(sys.argv) != 2:
    print("Provide an argument with the mazegen class name to test!")
    print("Accepted class names: [IRK_Gen, DFSGen, WilsonsGen]")
    sys.exit(1)

raw_arg_name = sys.argv[1]

if raw_arg_name not in ["IRK_Gen", "DFSGen", "WilsonsGen"]:
    print("Accepted class names: [IRK_Gen, DFSGen, WilsonsGen]")
    sys.exit(1)

for width, height in SIZES:
    for perfect in (True, False):
        path = Path(
            f"/tmp/{raw_arg_name.lower()}_{width}x{height}_{perfect}.txt"
        )

        maze = Maze(
            Point(width, height),
            Point(0, 0),
            Point(width - 1, height - 1),
        )
        generator: MazeGenerator
        if raw_arg_name == "IRK_Gen":
            generator = IRK_Gen(maze, perfect, Random(42))
        elif raw_arg_name == "DFSGen":
            generator = DFSGen(maze, perfect, Random(42))
        elif raw_arg_name == "WilsonsGen":
            generator = WilsonsGen(maze, perfect, Random(42))
        generator.finish()
        path.write_text(str(maze), encoding="utf-8")

        print(f"=== {width}x{height}, PERFECT={perfect} ===")
        result = run(
            [
                "uv",
                "run",
                "python",
                str(ANALYZER),
                str(path),
                "--min-loops",
                "0",
                "--max-dead-ends",
                str(width * height),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr, file=sys.stderr)
            sys.exit(result.returncode)
