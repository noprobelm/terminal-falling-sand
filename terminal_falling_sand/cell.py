from .cell_state import State
from .coordinates import Coordinate, MooreNeighborhood


class Cell:
    def __init__(
        self,
        coord: Coordinate,
        max_coord: Coordinate,
        state: State,
        color: str,
    ):
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
