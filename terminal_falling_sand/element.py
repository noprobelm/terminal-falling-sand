from __future__ import annotations
from dataclasses import dataclass
from rich.console import Console, ConsoleOptions, RenderResult
from random import randint
from rich.text import Text


@dataclass(eq=True, order=True, frozen=True)
class Coordinate:
    x: int
    y: int

    def __add__(self, other: Coordinate) -> Coordinate:
        return Coordinate(self.x + other.x, self.y + other.y)


@dataclass
class Element:
    coordinate: Coordinate

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        yield " "


@dataclass
class Empty(Element):
    def __post_init__(self):
        self._text = Text("▄", style="black", end="")
        self._color = "black"

    def step(self, neighbors: dict[str, Element]):
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

    def step(self, neighbors: dict[str, Element]):
        if isinstance(neighbors.get("LOWER"), Empty):
            return {
                self.coordinate: Empty(self.coordinate),
                neighbors["LOWER"].coordinate: MovableSolid(
                    neighbors["LOWER"].coordinate
                ),
            }
        if randint(1, 2) == 1:
            if isinstance(neighbors.get("LOWER_LEFT"), Empty):
                return {
                    self.coordinate: Empty(self.coordinate),
                    neighbors["LOWER_LEFT"].coordinate: MovableSolid(
                        neighbors["LOWER_LEFT"].coordinate
                    ),
                }
        elif isinstance(neighbors.get("LOWER_RIGHT"), Empty):
            return {
                self.coordinate: Empty(self.coordinate),
                neighbors["LOWER_RIGHT"].coordinate: MovableSolid(
                    neighbors["LOWER_RIGHT"].coordinate
                ),
            }

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        yield self._text
