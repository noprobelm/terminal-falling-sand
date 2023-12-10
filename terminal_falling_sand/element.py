from __future__ import annotations
from dataclasses import dataclass
from random import randint
from enum import Enum
from .state import State, MovableSolid, Empty


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


class Element:
    def __init__(self, coord: Coordinate, state: State, xmax: int, ymax: int):
        self.coord = coord
        self.state = state
        self._neighbors = {}
        for n in MooreNeighborhood:
            c = self.coord + Coordinate(*n.value)
            if (0 <= c.x <= xmax) and (0 <= c.y <= ymax):
                self._neighbors[n.name] = c

    def step(self, ref):
        neighbors = {}
        for n in self._neighbors:
            c = self._neighbors[n]
            neighbors[n] = ref[c.y][c.x]

        if isinstance(self.state, Empty) and all(
            isinstance(neighbors[n], Empty) for n in neighbors
        ):
            return

        if isinstance(self.state, MovableSolid):
            if "LOWER" in neighbors.keys() and isinstance(
                neighbors["LOWER"].state, Empty
            ):
                n = neighbors["LOWER"]
                n_color = n.state._color
                self_color = self.state._color
                ref[n.coord.y][n.coord.x].state = MovableSolid(self_color)
                ref[self.coord.y][self.coord.x].state = Empty(n_color)
                return
            elif (
                "LOWER_LEFT" in neighbors.keys()
                and "LOWER_RIGHT" in neighbors.keys()
                and isinstance(neighbors["LOWER_LEFT"].state, Empty)
                and isinstance(neighbors["LOWER_RIGHT"].state, Empty)
            ):
                candidates = [
                    neighbors["LOWER_LEFT"],
                    neighbors["LOWER_RIGHT"],
                ]
                n = candidates[randint(0, 1)]
                n_color = n.state._color
                self_color = self.state._color
                ref[n.coord.y][n.coord.x].state = MovableSolid(self_color)
                ref[self.coord.y][self.coord.x].state = Empty(n_color)

            elif "LOWER_LEFT" in neighbors.keys() and isinstance(
                neighbors["LOWER_LEFT"].state, Empty
            ):
                n = neighbors["LOWER_LEFT"]
                n_color = n.state._color
                self_color = self.state._color
                ref[n.coord.y][n.coord.x].state = MovableSolid(self_color)
                ref[self.coord.y][self.coord.x].state = Empty(n_color)

            elif "LOWER_RIGHT" in neighbors.keys() and isinstance(
                neighbors["LOWER_RIGHT"].state, Empty
            ):
                n = neighbors["LOWER_RIGHT"]
                n_color = n.state._color
                self_color = self.state._color
                ref[n.coord.y][n.coord.x].state = MovableSolid(self_color)
                ref[self.coord.y][self.coord.x].state = Empty(n_color)

        self._updated = True
