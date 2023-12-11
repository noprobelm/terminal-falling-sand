"""Hosts the CellState class and its various subclasses"""

from random import randint
from typing import Optional

from .coordinates import Coordinate, Neighbors


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

    def change_state(self, neighbors: Neighbors, matrix: list) -> Optional[Coordinate]:
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
        super().__init__(weight)

    def change_state(self, neighbors: Neighbors, matrix: list) -> Optional[Coordinate]:
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

        super().__init__(weight)

    def change_state(self, neighbors: Neighbors, matrix: list) -> Optional[Coordinate]:
        """Defines the behavior of a MovableSolid

        A MovableSolid's behavior can be defined as:
            - If it weighs more than the cell below it, swap states
            - Else if it weighs more than the cells below and diagonally left and right, pick one at random to swap with
            - Else if it weighs more than of the neighbors below and diagonally left and right, swap states
            - Else, retain state. Return None

        Args:
            neighbors (dict[str, CellState]): A map of MooreNeighborhood variants to their respective cell's state
        """

        for i in ["LOWER", ["LOWER_LEFT", "LOWER_RIGHT"], "LOWER_LEFT", "LOWER_RIGHT"]:
            if isinstance(i, str):
                c = getattr(neighbors, i)
                if c is not None:
                    state = matrix[c.y][c.x].state
                    if self.weight > state.weight:
                        return c
            elif isinstance(i, list):
                coords = [getattr(neighbors, k) for k in i]
                if any(c is None for c in coords):
                    continue
                states = [matrix[k.y][k.x].state for k in coords]
                if all(self.weight > state.weight for state in states):
                    return coords[randint(0, 1)]


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
        super().__init__(weight)

    def change_state(self, neighbors: Neighbors, matrix: list) -> Optional[Coordinate]:
        """Defines the behavior of a Liquid

        A MovableSolid's behavior can be defined as:
            - Explore all paths we would explore with the MovableSolid
            - Else if none of these are available, look left and right for valid candidates to move to
            - Else, retain state. Return None

        Args:
            neighbors (dict[str, CellState]): A map of MooreNeighborhood variants to their respective cell's state
        """

        for neighbor in [
            "LOWER",
            ["LOWER_LEFT", "LOWER_RIGHT"],
            "LOWER_LEFT",
            "LOWER_RIGHT",
            ["LEFT", "RIGHT"],
            "LEFT",
            "RIGHT",
        ]:
            if isinstance(neighbor, str):
                c = getattr(neighbors, neighbor)
                if c is not None and self.weight > matrix[c.y][c.x].state.weight:
                    return c
            elif isinstance(neighbor, list):
                coords = [getattr(neighbors, k) for k in neighbor]
                if any(c is None for c in coords):
                    continue
                states = [matrix[c.y][c.x].state for c in coords]
                if all(self.weight > state.weight for state in states):
                    return coords[randint(0, 1)]
