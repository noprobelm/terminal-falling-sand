"""Hosts the base Cell class used in the simulation"""

from .cell_state import CellState
from .coordinates import Coordinate, MooreNeighborhood


class Cell:
    """This class acts as the base Cell class for the simulation

    All cells participating in the CellMatrix simulation should ultimatleyb e derived from this class. Refer to the
    'elements' module for the public facing API (the details of an element should be defined there)

    Attributes:
        coord (Coordinate): The coordinate of the cell
        max_coord (Coordinate): The maximum possible coordinate for a cell. Used to identify valid neighbors
        _neighbors (dict[str, Coordinate]): A dictionary of MooreNeighboorhood enum variants to their respective coord
    """

    def __init__(
        self,
        coord: Coordinate,
        max_coord: Coordinate,
        state: CellState,
        color: str,
    ):
        """Initializes an instance of Cell

        Args:
            coord (Coordinate): The coordinate of the cell
            max_coord (Coordinate): The maximum possible coordinate for a cell. Used to identify valid neighbors
            state (CellState): The CellState we should defer to for a cell's behavior
            color (str): The color of the cell. Hex or standard color names are acceptable here
        """
        self.coord = coord
        self.state = state
        self.color = color
        self._neighbors = {}
        for n in MooreNeighborhood:
            c = self.coord + Coordinate(*n.value)
            if (0 <= c.x <= max_coord.x) and (0 <= c.y <= max_coord.y):
                self._neighbors[n.name] = c

    def step(self, matrix):
        neighbors = {}
        for n in self._neighbors:
            c = self._neighbors[n]
            neighbors[n] = matrix[c.y][c.x]

        new = self.state.change_state(neighbors)
        if new:
            old_color = self.color
            new_color = matrix[new[0].y][new[0].x].color
            old_state = self.state

            matrix[self.coord.y][self.coord.x].color = new_color
            matrix[self.coord.y][self.coord.x].state = new[1]

            matrix[new[0].y][new[0].x].color = old_color
            matrix[new[0].y][new[0].x].state = old_state
