"""Hosts the base Cell class used in the simulation"""

from typing import Optional

from .cell_state import CellState
from .coordinate import Coordinate, MooreNeighborhood, Neighbors


class Cell:
    """This class acts as the base Cell class for the simulation

    All cells participating in the CellMatrix simulation should ultimatleyb e derived from this class. Refer to the
    'elements' module for the public facing API (the details of an element should be defined there)

    Attributes:
        state (CellState): The state the cell is in
        neighbors (Neighbors): Stores MooreNeighboorhood enum variants to their respective coord
    """

    def __init__(
        self,
        coord: Coordinate,
        max_coord: Coordinate,
        state: CellState,
    ) -> None:
        """Initializes an instance of Cell

        Args:
            coord (Coordinate): The coordinate of the cell
            max_coord (Coordinate): The maximum possible coordinate for a cell. Used to identify valid neighbors
            state (CellState): The CellState we should defer to for a cell's behavior
            color (str): The color of the cell. Hex or standard color names are acceptable here
        """
        self.state = state
        neighbors = []
        for nc in MooreNeighborhood:
            c = coord + nc.value
            if (0 <= c.x <= max_coord.x) and (0 <= c.y <= max_coord.y):
                neighbors.append(c)
            else:
                neighbors.append(None)

        self.neighbors = Neighbors(*neighbors)
        self.updated = False

    @property
    def ignore(self):
        """Interface for state.ignore"""
        return self.state.ignore

    @property
    def color(self):
        """Interface for state.color"""
        return self.state.color

    @property
    def weight(self):
        """Interface for state.weight"""
        return self.state.weight

    def change_state(self, matrix: list) -> Optional[Coordinate]:
        """Steps the cell forward based on the parameters of its neighbors

        If the cell's state changes, swap its color and state with the target neighbor.

        Args:
            matrix (list): The underlying list of elements found in the CellMatrix
        """

        if self.ignore is True or self.updated is True:
            return

        neighbor = self.state.change_state(self.neighbors, matrix)
        if neighbor is not None:
            neighbor = matrix[neighbor.y][neighbor.x]
            old_state = self.state
            self.state = neighbor.state
            neighbor.state = old_state
            neighbor.updated = True

        self.updated = True
