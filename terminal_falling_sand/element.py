from __future__ import annotations
from dataclasses import dataclass
from rich.console import Console, ConsoleOptions, RenderResult
from random import randint
from rich.text import Text
from enum import Enum
from .state import State


class MooreNeighborhood(Enum):
    UPPER_LEFT = (-1, -1)
    UPPER = (0, -1)
    UPPER_RIGHT = (1, -1)
    RIGHT = (1, 0)
    LOWER_RIGHT = (1, 1)
    LOWER = (0, 1)
    LOWER_LEFT = (-1, 1)
    LEFT = (-1, 0)


@dataclass(eq=True, order=True, frozen=True)
class Coordinate:
    x: int
    y: int

    def __add__(self, other: Coordinate) -> Coordinate:
        return Coordinate(self.x + other.x, self.y + other.y)


@dataclass
class Element:
    coordinate: Coordinate
    state: State

    def step(self, ref):
        neighbors = {}
        for n in MooreNeighborhood:
            c = self.coordinate + Coordinate(*n.value)
            neighbors[n.name] = ref[c.y][c.x].state

        self.state = self.state.step(neighbors)
