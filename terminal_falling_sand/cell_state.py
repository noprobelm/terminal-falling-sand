"""Hosts the CellState class and its various subclasses"""

from random import randint
from typing import Optional

from .coordinates import Coordinate


class CellState:
    """Base class for a cell's state

    Attributes:
        weight (int): Usually influences whether a cell should move in the direction it's looking. The usage of this
                      attr can vary between subclasses
    """

    def __init__(self, weight: int) -> None:
        """Initializes an instance of the CellState class

        Args:
            weight (int): The weight of the cell
        """
        self.weight = weight

    def _map_neighbor_states(self, neighbors: dict[str, Coordinate], matrix):
        neighbor_states = {}
        for n in neighbors:
            c = neighbors[n]
            neighbor_states[n] = matrix[c.y][c.x].state
        return neighbor_states

    def change_state(
        self, neighbors: dict[str, Coordinate], matrix: list
    ) -> Optional[Coordinate]:
        """Dictates the behavior of a cell's state

        This should be filled out in subclass instances to dictate the desired behavior of a cell

        If a cell changes state, the cell it's swapping with should be returned as a tuple of its coordinates and state

        Args:
            neighbors (dict[str, CellState]): A map of MooreNeighborhood variants to their respective cell's state
        """


class Empty(CellState):
    """Placeholder for empty values in a CellMatrix simulation.

    This is functionally equivalent to the CellState class, but should preferred when representing Empty cells

    Attributes:
        weight (int): The cell's weight
    """

    def __init__(self, weight: int) -> None:
        """Initializes an instance of the Empty class

        Args:
            weight (int): The weight of the cell

        """
        self.weight = weight
        pass

    def change_state(
        self, neighbors: dict[str, Coordinate], matrix: list
    ) -> Optional[Coordinate]:
        """Defines the behavior of the Empty cell

        The 'Empty' CellState has no behavior

        Args:
            neighbors (dict[str, CellState]): A map of MooreNeighborhood variants to their respective cell's state
        """


class MovableSolid(CellState):
    """Defines behavior for movable solids

    Attributes:
        weight (int): The weight of the cell
    """

    def __init__(self, weight: int):
        """Initializes an instance of the MovableSolid class

        Args:
            weight (int): The weight of the cell

        """

        self.weight = weight

    def change_state(
        self, neighbors: dict[str, Coordinate], matrix: list
    ) -> Optional[Coordinate]:
        """Defines the behavior of a MovableSolid

        A MovableSolid's behavior can be defined as:
            - If it weighs more than the cell below it, swap states
            - Else if it weighs more than the cells below and diagonally left and right, pick one at random to swap with
            - Else if it weighs more than of the neighbors below and diagonally left and right, swap states
            - Else, retain state. Return None

        Args:
            neighbors (dict[str, CellState]): A map of MooreNeighborhood variants to their respective cell's state
        """

        neighbor_states = self._map_neighbor_states(neighbors, matrix)
        if "LOWER" in neighbor_states and self.weight > neighbor_states["LOWER"].weight:
            return neighbors["LOWER"]

        elif (
            "LOWER_LEFT" in neighbor_states
            and "LOWER_RIGHT" in neighbor_states
            and self.weight > neighbor_states["LOWER_LEFT"].weight
            and self.weight > neighbor_states["LOWER_RIGHT"].weight
        ):
            neighbor = ["LOWER_LEFT", "LOWER_RIGHT"][randint(0, 1)]
            return neighbors[neighbor]

        elif (
            "LOWER_LEFT" in neighbor_states
            and self.weight > neighbor_states["LOWER_LEFT"].weight
        ):
            return neighbors["LOWER_LEFT"]

        elif (
            "LOWER_RIGHT" in neighbor_states
            and self.weight > neighbor_states["LOWER_RIGHT"].weight
        ):
            return neighbors["LOWER_RIGHT"]
        else:
            return None

        return neighbors[neighbor]


class Liquid(CellState):
    """Defines behavior for liquids

    Args:
        weight (int): The weight of the cell
    """

    def __init__(self, weight: int):
        """Initializes an instance of the Liquid class

        Args:
            weight (int): The weight of the cell

        """
        self.weight = weight

    def change_state(
        self, neighbors: dict[str, Coordinate], matrix: list
    ) -> Optional[Coordinate]:
        """Defines the behavior of a Liquid

        A MovableSolid's behavior can be defined as:
            - Explore all paths we would explore with the MovableSolid
            - Else if none of these are available, look left and right for valid candidates to move to
            - Else, retain state. Return None

        Args:
            neighbors (dict[str, CellState]): A map of MooreNeighborhood variants to their respective cell's state
        """

        neighbor_states = self._map_neighbor_states(neighbors, matrix)

        if "LOWER" in neighbor_states and self.weight > neighbor_states["LOWER"].weight:
            return neighbors["LOWER"]

        elif (
            "LOWER_LEFT" in neighbor_states
            and "LOWER_RIGHT" in neighbor_states
            and self.weight > neighbor_states["LOWER_LEFT"].weight
            and self.weight > neighbor_states["LOWER_RIGHT"].weight
        ):
            neighbor = ["LOWER_LEFT", "LOWER_RIGHT"][randint(0, 1)]
            return neighbors[neighbor]

        elif (
            "LOWER_LEFT" in neighbor_states
            and self.weight > neighbor_states["LOWER_LEFT"].weight
        ):
            return neighbors["LOWER_LEFT"]

        elif (
            "LOWER_RIGHT" in neighbor_states
            and self.weight > neighbor_states["LOWER_RIGHT"].weight
        ):
            return neighbors["LOWER_RIGHT"]

        elif (
            "LEFT" in neighbor_states
            and "RIGHT" in neighbor_states
            and self.weight > neighbor_states["LEFT"].weight
            and self.weight > neighbor_states["RIGHT"].weight
        ):
            neighbor = ["LEFT", "RIGHT"][randint(0, 1)]
            return neighbors[neighbor]

        elif "LEFT" in neighbor_states and self.weight > neighbor_states["LEFT"].weight:
            return neighbors["LEFT"]

        elif (
            "RIGHT" in neighbor_states and self.weight > neighbor_states["RIGHT"].weight
        ):
            return neighbors["RIGHT"]
