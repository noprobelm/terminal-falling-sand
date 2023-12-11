"""Hosts the CellMatrix class used to run the simulation"""

from typing import Type

from rich.console import Console, ConsoleOptions
from rich.segment import Segment
from rich.style import Style

from .coordinates import Coordinate
from .elements import ElementType, Empty


class CellMatrix(list):
    """This class acts as the directory for all elements in the simulation

    Since the matrix will always be continuous ('Empty' elements represent empty space), we subclass from list to enable
    efficient lookup of elements. A dictionary-like structure would usually be less efficient, especially when updating
    values, due to the necessity of rehashing keys.

    Attributes:
        max_coord (Coordinate): The maximum valid coordinate found in the grid
        midpoint (Coordinate): The midpoint of the grid.

    """

    def __init__(self, xmax: int, ymax: int) -> None:
        """Initializes a CellMatrix instance

        Generates a new grid full of 'Empty' elements

        Args:
            xmax (int): The maximum x value in the grid
            ymax (int): The maximum y value in the grid

        """
        matrix = []
        self.max_coord = Coordinate(xmax - 1, ymax - 1)
        self.midpoint = self.max_coord.x // 2
        if self.midpoint % 2 == 1:
            self.midpoint += 1

        for y in range(ymax):
            matrix.append([])
            for x in range(xmax):
                coord = Coordinate(x, y)
                matrix[coord.y].append(Empty(coord, self.max_coord))
        super().__init__(matrix)

    def spawn(self, element: Type[ElementType], x: int, y: int) -> None:
        """Spawns an element at a given x/y coordinate

        Args:
            element (ElementType): An 'ElementType' type
            x (int): The x coordinate of the element to be spawned
            y (int): The y coordinate of the element to be spawned
        """

        coord = Coordinate(x, y)
        self[y][x] = element(coord, self.max_coord)

    def step(self):
        for y in range(self.max_coord.y + 1):
            for x1 in range(0, self.midpoint + 1):
                self[self.max_coord.y - y][x1].step(self)
            for x2 in range(self.midpoint, self.max_coord.x + 1):
                self[self.max_coord.y - y][self.max_coord.x - x2 - self.midpoint].step(
                    self
                )

    def __rich_console__(self, console: Console, options: ConsoleOptions):
        for y in range(self.max_coord.y)[::2]:
            for x in range(self.max_coord.x + 1):
                bg = self[y][x].color
                fg = self[y + 1][x].color
                yield Segment("▄", Style(color=fg, bgcolor=bg))
            yield Segment.line()
