"""Hosts the base Cell class used in the simulation"""

from .cell_state import CellState
from .coordinates import Coordinate, MooreNeighborhood
from typing import Optional


class Cell:
    """This class acts as the base Cell class for the simulation

    All cells participating in the CellMatrix simulation should ultimatleyb e derived from this class. Refer to the
    'elements' module for the public facing API (the details of an element should be defined there)

    Attributes:
        state (CellState): The state a cell is in
        color (str): The color of a cell
        _neighbors (dict[str, Coordinate]): A dictionary of MooreNeighboorhood enum variants to their respective coord
    """

    def __init__(
        self,
        coord: Coordinate,
        max_coord: Coordinate,
        state: CellState,
        color: str,
    ) -> None:
        """Initializes an instance of Cell

        Args:
            coord (Coordinate): The coordinate of the cell
            max_coord (Coordinate): The maximum possible coordinate for a cell. Used to identify valid neighbors
            state (CellState): The CellState we should defer to for a cell's behavior
            color (str): The color of the cell. Hex or standard color names are acceptable here
        """
        self.state = state
        self.color = color
        self._neighbors = {}
        for n in MooreNeighborhood:
            c = coord + Coordinate(*n.value)
            if (0 <= c.x <= max_coord.x) and (0 <= c.y <= max_coord.y):
                self._neighbors[n.name] = c

    def change_state(self, matrix: list) -> Optional[Coordinate]:
        """Steps the cell forward based on the parameters of its neighbors

        If the cell's state changes, swap its color and state with the target neighbor.

        Args:
            matrix (list): The underlying list element of the CellMatrix
        """
        neighbor = self.state.change_state(self._neighbors, matrix)
        if neighbor:
            old_state = self.state
            old_color = self.color
            self.color = matrix[neighbor.y][neighbor.x].color
            self.state = matrix[neighbor.y][neighbor.x].state
            matrix[neighbor.y][neighbor.x].color = old_color
            matrix[neighbor.y][neighbor.x].state = old_state
