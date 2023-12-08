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
        if isinstance(neighbors.get("UPPER").state, MovableSolid):
            return neighbors.get("UPPER").state
        if randint(1, 2) == 1:
            if isinstance(neighbors.get("UPPER_LEFT").state, MovableSolid):
                return neighbors.get("UPPER_LEFT").state
        elif isinstance(neighbors.get("UPPER_RIGHT").state, MovableSolid):
            return neighbors.get("UPPER_RIGHT").state

        return self


@dataclass
class MovableSolid(State):
    def __post_init__(self):
        self._text = Text("▄", style="yellow3", end="")
        self._color = "yellow3"

    def step(self, neighbors):
        if isinstance(neighbors.get("LOWER").state, Empty):
            return neighbors.get("LOWER").state
        if randint(1, 2) == 1:
            if isinstance(neighbors.get("LOWER_LEFT").state, Empty):
                return neighbors.get("LOWER_LEFT").state
        elif isinstance(neighbors.get("LOWER_RIGHT").state, Empty):
            return neighbors.get("LOWER_RIGHT").state

        return self
