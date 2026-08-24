class Maze:
    def __init__(
        self,
        size: tuple[int, int],
        entry: tuple[int, int],
        exit: tuple[int, int],
    ) -> None:
        if (
            entry[0] < 0
            or entry[1] < 0
            or entry[0] >= size[0]
            or entry[1] >= size[1]
        ):
            raise ValueError("Entry point outside maze structure")
        if (
            exit[0] < 0
            or exit[1] < 0
            or exit[0] >= size[0]
            or exit[1] >= size[1]
        ):
            raise ValueError("Exit point outside maze structure")
        self._size = size
        self._entry = entry
        self._exit = exit

    #        self._maze = ((Cell) for x in )

    @property
    def size(self) -> tuple[int, int]:
        return self._size

    @property
    def entry(self) -> tuple[int, int]:
        return self._entry

    @property
    def exit(self) -> tuple[int, int]:
        return self._exit
