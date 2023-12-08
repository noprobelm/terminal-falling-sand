from __future__ import annotations
from dataclasses import dataclass
from rich.console import Console, ConsoleOptions, RenderResult
from random import randint
from rich.text import Text
from enum import Enum


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

    @property
    def neighbors(self):
        return self._neighbors

    @neighbors.setter
    def neighbors(self, c: Coordinate):
        neighbors = {}
        for n in MooreNeighborhood:
            nc = self.coordinate + Coordinate(*n.value)
            if nc.x >= 0 and nc.x <= c.x and nc.y >= 0 and nc.y <= c.y:
                neighbors[n.name] = nc

        self._neighbors = neighbors

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        yield " "


@dataclass
class Empty(Element):
    def __post_init__(self):
        self._text = Text("▄", style="black", end="")
        self._color = "black"

    def step(self, neighbors):
        return {}

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        yield self._text


@dataclass
class MovableSolid(Element):
    def __post_init__(self):
        self._text = Text("▄", style="yellow3", end="")
        self._color = "yellow3"

    def step(self, neighbors):
        if isinstance(self.neighbors.get("LOWER"), Empty):
            return {
                self.coordinate: Empty(self.coordinate),
                self.neighbors["LOWER"].coordinate: MovableSolid(
                    self.neighbors["LOWER"].coordinate
                ),
            }
        if randint(1, 2) == 1:
            if isinstance(self.neighbors.get("LOWER_LEFT"), Empty):
                return {
                    self.coordinate: Empty(self.coordinate),
                    self.neighbors["LOWER_LEFT"].coordinate: MovableSolid(
                        self.neighbors["LOWER_LEFT"].coordinate
                    ),
                }
        elif isinstance(self.neighbors.get("LOWER_RIGHT"), Empty):
            return {
                self.coordinate: Empty(self.coordinate),
                self.neighbors["LOWER_RIGHT"].coordinate: MovableSolid(
                    self.neighbors["LOWER_RIGHT"].coordinate
                ),
            }

        return {}

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        yield self._text
