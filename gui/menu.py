from abc import ABC, abstractmethod
from gui.program import State


class Menu(ABC):
    @abstractmethod
    def handle_keys(key: int, state: State) -> None:
        ...
    @abstractmethod
    def draw(state: State) -> None:
        ...
