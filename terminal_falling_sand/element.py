from __future__ import annotations
from dataclasses import dataclass
from rich.console import Console, ConsoleOptions, RenderResult
from random import randint
from rich.text import Text
from enum import Enum
from .state import State, MovableSolid, Empty
import time


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
    xmax: int
    ymax: int

    def __post_init__(self):
        self._updated = False
        self._neighbors = {}
        for n in MooreNeighborhood:
            c = self.coordinate + Coordinate(*n.value)
            if (0 <= c.x <= self.xmax) and (0 <= c.y <= self.ymax):
                self._neighbors[n.name] = c

    def step(self, ref):
        if not isinstance(self.state, MovableSolid) or self._updated == True:
            return

        neighbors = {}
        for n in self._neighbors:
            c = self._neighbors[n]
            neighbors[n] = ref[c.y][c.x]

        if "LOWER" in neighbors and isinstance(neighbors["LOWER"].state, Empty):
            n = neighbors["LOWER"]
            ref[n.coordinate.y][n.coordinate.x].state = MovableSolid()
            ref[n.coordinate.y][n.coordinate.x]._updated = True
            ref[self.coordinate.y][self.coordinate.x].state = Empty()
            self._updated = True
        elif (
            randint(0, 1) == 0
            and "LOWER_LEFT" in neighbors
            and isinstance(neighbors["LOWER_LEFT"].state, Empty)
        ):
            n = neighbors["LOWER_LEFT"]
            ref[n.coordinate.y][n.coordinate.x].state = MovableSolid()
            ref[n.coordinate.y][n.coordinate.x]._updated = True
            ref[self.coordinate.y][self.coordinate.x].state = Empty()
            self._updated = True
        elif "LOWER_RIGHT" in neighbors and isinstance(
            neighbors["LOWER_RIGHT"].state, Empty
        ):
            n = neighbors["LOWER_RIGHT"]
            ref[n.coordinate.y][n.coordinate.x].state = MovableSolid()
            ref[n.coordinate.y][n.coordinate.x]._updated = True
            ref[self.coordinate.y][self.coordinate.x].state = Empty()
            self._updated = True

        self._updated = True
