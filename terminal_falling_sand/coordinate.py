"""The coordinate system used by the CellMatrix simulation

Includes the Neighbors namedtuple, which is used in the cell and cell_state modules
"""

from __future__ import annotations

from collections import namedtuple
from dataclasses import dataclass
from enum import Enum


@dataclass(eq=True, order=True, frozen=True, slots=True)
class Coordinate:
    """An x/y coordinate to reference location in a CellMatrix"""

    x: int
    y: int

    def __add__(self, other: Coordinate) -> Coordinate:
        """Returns the sum of one coordinate and another. Primarily used to identify neighbors"""
        return Coordinate(self.x + other.x, self.y + other.y)


class MooreNeighborhood(Enum):
    """Enumeration for variants of neighbors found in a Moore Neighborhood"""

    UPPER_LEFT = Coordinate(-1, -1)
    UPPER = Coordinate(0, -1)
    UPPER_RIGHT = Coordinate(1, -1)
    RIGHT = Coordinate(1, 0)
    LOWER_RIGHT = Coordinate(1, 1)
    LOWER = Coordinate(0, 1)
    LOWER_LEFT = Coordinate(-1, 1)
    LEFT = Coordinate(-1, 0)


Neighbors = namedtuple("Neighbors", [member.name for member in MooreNeighborhood])
