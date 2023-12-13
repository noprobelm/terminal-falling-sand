"""Hosts the CellMatrix class used to run the simulation"""

from typing import Type

from rich.console import Console, ConsoleOptions, RenderResult
from rich.segment import Segment
from rich.style import Style

from .coordinate import Coordinate
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

    def spawn(self, element: Type[ElementType], coord: Coordinate) -> None:
        """Spawns an element at a given x/y coordinate

        Args:
            element (ElementType): An 'ElementType' type
            coord (Coordinate): The coordinate to spawn the element at
        """

        self[coord.y][coord.x] = element(coord, self.max_coord)

    def step(self) -> None:
        """Steps the simulation forward once

        Explores every element in the simulation by working bottom to top, then left -> middle; right -> middle for each
        row. Each step in the simulation calls the 'step' method on the underlying Cell type. Cell.step will determien
        its next place in the CellMatrix and modify the CellMatrix reference passed to it accordingly.

        Issue:
            When we step each element from left -> right or right -> left, the elements on the trailing end exhibit odd
            behavior. Specifically, elements will move diagonally and to the left (or right) depending on the order
            we're stepping them in. Unsure of the exact cause of this, but for now, working "middle out" in either
            direction visually solves the problem. This probably means there's some odd behavior in the middle of the
            matrix for each step, but it's not visually identifiable. Working "middle out" is an acceptable workaround
            for now.

        After each cell has been stepped through, reset its updated flag to False
        """

        for y in range(self.max_coord.y + 1):
            row = self.max_coord.y - y
            for x in range(self.midpoint + 1):
                element = self[row][x]
                if element.ignore is False or element.updated is False:
                    element.change_state(self)

            midpoint_offset = self.max_coord.x - self.midpoint
            for x in range(self.midpoint, self.max_coord.x + 1):
                element = self[row][midpoint_offset - x]
                if element.ignore is False or element.updated is False:
                    element.change_state(self)

        for y in range(self.max_coord.y + 1):
            row = self.max_coord.y - y
            for x in range(self.max_coord.x + 1):
                self[row][x].updated = False

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        """Renders each Cell in the simulation using the Rich Console Protocol

        Due to the typical 2:1 height/width aspect ratio of a terminal, each cell rendered from the CellMatrix simulation
        actually occupies 2 rows in the terminal. I picked up this trick from rich's __main__ module. Run
        'python -m rich and observe the color palette at the top of stdout for another example of what this refers to.

        Yields:
            2 cells in the simulation, row by row, until all cell states have been rendered.
        """
        for y in range(self.max_coord.y)[::2]:
            for x in range(self.max_coord.x + 1):
                bg = self[y][x].color
                fg = self[y + 1][x].color
                yield Segment("▄", Style(color=fg, bgcolor=bg))
            yield Segment.line()
