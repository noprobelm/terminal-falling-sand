from dataclasses import dataclass
from random import randint
from .colors import SAND_COLORS
from typing import Optional


class State:
    def __init__(self, color: Optional[str] = None):
        if color is None:
            self._color = "black"
        else:
            self._color = color


class Empty(State):
    def __init__(self, color: Optional[str] = None):
        color = "black"
        super().__init__(color)


class MovableSolid(State):
    def __init__(self, color: Optional[str] = None):
        if color is None:
            color = SAND_COLORS[randint(0, len(SAND_COLORS) - 1)]
        super().__init__(color)
