"""Hosts the CellState class and its various subclasses"""

from random import randint
from typing import Optional

from .coordinate import Coordinate, Neighbors


class CellState:
    """Base class for a cell's state

    Attributes:
        weight (int): Usually influences whether a cell should move in the direction it's looking. The usage of this
                      attr can vary between subclasses
        color (str): The color to render the cell as
        ignore (bool): Should the change_state method run
    """

    def __init__(self, weight: int, color: str) -> None:
        """Initializes an instance of the CellState class

        Args:
            weight (int): The weight of the cell
            color (str): The color of the cell
        """
        self.weight = weight
        self.color = color
        self.ignore = False

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
        color (str): The color to render the cell as
        ignore (bool): Should the change_state method run

    """

    def __init__(self, weight: int, color: str) -> None:
        """Initializes an instance of the Empty class

        Args:
            weight (int): The weight of the cell
            color (str): The color of the cell

        """
        super().__init__(weight, color)
        self.ignore = True

    def change_state(self, neighbors: Neighbors, matrix: list) -> Optional[Coordinate]:
        """Defines the behavior of the Empty cell

        The 'Empty' CellState has no behavior

        Args:
            neighbors (dict[str, CellState]): A map of MooreNeighborhood variants to their respective cell's state
        """


class Solid(CellState):
    """Defines behavior for movable solids

    Attributes:
        weight (int): The cell's weight
        color (str): The color to render the cell as
        ignore (bool): Should the change_state method run
    """

    def __init__(self, weight: int, color: str):
        """Initializes an instance of the MovableSolid class

        Args:
            weight (int): The weight of the cell
            color (str): The color of the cell

        """

        super().__init__(weight, color)

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

        if (
            neighbors.LOWER is not None
            and self.weight > matrix[neighbors.LOWER.y][neighbors.LOWER.x].weight
        ):
            return neighbors.LOWER


class MovableSolid(CellState):
    """Defines behavior for movable solids

    Attributes:
        weight (int): The cell's weight
        color (str): The color to render the cell as
        ignore (bool): Should the change_state method run
    """

    def __init__(self, weight: int, color: str):
        """Initializes an instance of the MovableSolid class

        Args:
            weight (int): The weight of the cell
            color (str): The color of the cell

        """

        super().__init__(weight, color)

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

        for i in [
            neighbors.LOWER,
            (neighbors.LOWER_LEFT, neighbors.LOWER_RIGHT),
            neighbors.LOWER_LEFT,
            neighbors.LOWER_RIGHT,
        ]:
            if isinstance(i, tuple):
                candidates = []
                for n in i:
                    if n is not None and self.weight > matrix[n.y][n.x].weight:
                        candidates.append(n)
                    if len(candidates) == 2:
                        return candidates[randint(0, 1)]
            elif i is not None and self.weight > matrix[i.y][i.x].weight:
                return i


class Liquid(CellState):
    """Defines behavior for liquids

    Args:
        weight (int): The weight of the cell
    """

    def __init__(self, weight: int, color: str):
        """Initializes an instance of the Liquid class

        Args:
            weight (int): The weight of the cell

        """
        super().__init__(weight, color)

    def change_state(self, neighbors: Neighbors, matrix: list) -> Optional[Coordinate]:
        """Defines the behavior of a Liquid

        A MovableSolid's behavior can be defined as:
            - Explore all paths we would explore with the MovableSolid
            - Else if none of these are available, look left and right for valid candidates to move to
            - Else, retain state. Return None

        Args:
            neighbors (dict[str, CellState]): A map of MooreNeighborhood variants to their respective cell's state
        """

        for i in [
            neighbors.LOWER,
            (neighbors.LOWER_LEFT, neighbors.LOWER_RIGHT),
            neighbors.LOWER_LEFT,
            neighbors.LOWER_RIGHT,
            (neighbors.LEFT, neighbors.RIGHT),
            neighbors.LEFT,
            neighbors.RIGHT,
        ]:
            if isinstance(i, tuple):
                candidates = []
                for n in i:
                    if n is not None and self.weight > matrix[n.y][n.x].weight:
                        candidates.append(n)
                    if len(candidates) == 2:
                        return candidates[randint(0, 1)]
            elif i is not None and self.weight > matrix[i.y][i.x].weight:
                return i
