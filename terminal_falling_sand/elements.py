"""This module defines elements used directly by the CellMatrix simulation

The elements found in this module are derived from the Cell class. The CellMatrix simulation should consist only of
elements from this module
"""

from random import randint

from . import cell_state
from .cell import Cell
from .cell_state import CellState
from .colors import SAND_COLORS, WATER_COLORS
from .coordinates import Coordinate


class Element(Cell):
    """Base class for an element

    Attributes:
        coord (Coordinate): The coordinate of the cell
        max_coord (Coordinate): The maximum possible coordinate for a cell. Used to identify valid neighbors
        state (CellState): The state a cell is in
        color (str): The color of a cell
        _neighbors (dict[str, Coordinate]): A dictionary of MooreNeighboorhood enum variants to their respective coord
    """

    def __init__(
        self, coord: Coordinate, max_coord: Coordinate, state: CellState
    ) -> None:
        """Initializes an instance of the Element class

        Args:
            coord (Coordinate): The coordinate of the cell
            max_coord (Coordinate): The maximum possible coordinate for a cell. Used to identify valid neighbors
            state (CellState): The CellState we should defer to for a cell's behavior

        """
        super().__init__(coord, max_coord, state)


class ElementType:
    """Reserved for type hinting Element types in the CellMatrix class from the cell_matrix module"""

    def __init__(self, *args, **kwargs):
        """Initializes an instance of the ElementType class"""
        pass


class Empty(Element, ElementType):
    """An Empty element

    Attributes:
        coord (Coordinate): The coordinate of the cell
        max_coord (Coordinate): The maximum possible coordinate for a cell. Used to identify valid neighbors
        state (CellState): The state a cell is in

    """

    def __init__(self, coord: Coordinate, max_coord: Coordinate):
        """Initializes an instance of the Empty class

        - An Empty cell's color is set to "black" (the background of the terminal)

        Args:
            coord (Coordinate): The coordinate of the cell
            max_coord (Coordinate): The maximum possible coordinate for a cell. Used to identify valid neighbors

        """

        state = cell_state.Empty(weight=0, color="black")
        super().__init__(coord, max_coord, state)


class Sand(Element, ElementType):
    """A Sand element

    Attributes:
        coord (Coordinate): The coordinate of the cell
        max_coord (Coordinate): The maximum possible coordinate for a cell. Used to identify valid neighbors
        state (CellState): The state a cell is in

    """

    def __init__(self, coord: Coordinate, max_coord: Coordinate):
        """Initializes an instance of the Sand class

        - A Sand cell's color is set to one of those found among the SAND_COLORS dict

        Args:
            coord (Coordinate): The coordinate of the cell
            max_coord (Coordinate): The maximum possible coordinate for a cell. Used to identify valid neighbors

        """

        color = SAND_COLORS[randint(0, len(SAND_COLORS) - 1)]
        state = cell_state.MovableSolid(weight=2, color=color)
        super().__init__(coord, max_coord, state)


class Water(Element, ElementType):
    """A Water element

    Attributes:
        coord (Coordinate): The coordinate of the cell
        max_coord (Coordinate): The maximum possible coordinate for a cell. Used to identify valid neighbors
        state (CellState): The state a cell is in

    """

    def __init__(self, coord: Coordinate, max_coord: Coordinate):
        """Initializes an instance of the Water class

        - A Water cell's color is set to one of those found among the WATER_COLORS dict

        Args:
            coord (Coordinate): The coordinate of the cell
            max_coord (Coordinate): The maximum possible coordinate for a cell. Used to identify valid neighbors

        """

        color = WATER_COLORS[randint(0, len(WATER_COLORS) - 1)]
        state = cell_state.Liquid(weight=1, color=color)
        super().__init__(coord, max_coord, state)
