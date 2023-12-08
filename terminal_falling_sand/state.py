from typing import Callable
from enum import Enum
from dataclasses import dataclass
from rich.text import Text
from random import randint


@dataclass
class State:
    def step(self, neighbors):
        return self


@dataclass
class Empty(State):
    def __post_init__(self):
        self._text = Text("▄", style="black", end="")
        self._color = "black"

    def step(self, neighbors):
        if isinstance(neighbors.get("UPPER"), MovableSolid):
            return neighbors.get("UPPER")
        if randint(1, 2) == 1:
            if isinstance(neighbors.get("UPPER_LEFT"), MovableSolid):
                return neighbors.get("UPPER_LEFT")
        elif isinstance(neighbors.get("UPPER_RIGHT"), MovableSolid):
            return neighbors.get("UPPER_RIGHT")

        return self


@dataclass
class MovableSolid(State):
    def __post_init__(self):
        self._text = Text("▄", style="yellow3", end="")
        self._color = "yellow3"

    def step(self, neighbors):
        if isinstance(neighbors.get("LOWER"), Empty):
            return neighbors.get("LOWER")
        if randint(1, 2) == 1:
            if isinstance(neighbors.get("LOWER_LEFT"), Empty):
                return neighbors.get("LOWER_LEFT")
        elif isinstance(neighbors.get("LOWER_RIGHT"), Empty):
            return neighbors.get("LOWER_RIGHT")

        return self
