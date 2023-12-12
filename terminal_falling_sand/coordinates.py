"""The coordinate system used by the CellMatrix simulation"""

from __future__ import annotations

from collections import namedtuple
from dataclasses import dataclass
from enum import Enum


class MooreNeighborhood(Enum):
    """Enumeration for variants of neighbors found in a Moore Neighborhood"""

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
    """An x/y coordinate to reference location in a CellMatrix"""

    x: int
    y: int

    def __add__(self, other: Coordinate) -> Coordinate:
        """Returns the sum of one coordinate and another. Primarily used to identify neighbors"""
        return Coordinate(self.x + other.x, self.y + other.y)


Neighbors = namedtuple("Neighbors", [member.name for member in MooreNeighborhood])
