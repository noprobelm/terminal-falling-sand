from random import randint
from .cell_state import State, MovableSolid
from .coordinates import Coordinate, MooreNeighborhood


class Cell:
    def __init__(
        self, coord: Coordinate, max_coord: Coordinate, state: State, color: str
    ):
        self.coord = coord
        self.state = state
        self.color = color
        self._neighbors = {}
        for n in MooreNeighborhood:
            c = self.coord + Coordinate(*n.value)
            if (0 <= c.x <= max_coord.x) and (0 <= c.y <= max_coord.y):
                self._neighbors[n.name] = c

    def step(self, ref):
        neighbors = {}
        for n in self._neighbors:
            c = self._neighbors[n]
            neighbors[n] = ref[c.y][c.x]

        if isinstance(self.state, Empty) and all(
            isinstance(neighbors[n], Empty) for n in neighbors
        ):
            return

        if isinstance(self.state, MovableSolid):
            if "LOWER" in neighbors.keys() and isinstance(
                neighbors["LOWER"].state, Empty
            ):
                n = neighbors["LOWER"]
                n_color = n.state._color
                self_color = self.state._color
                ref[n.coord.y][n.coord.x].state = MovableSolid(self_color)
                ref[self.coord.y][self.coord.x].state = Empty(n_color)
                return
            elif (
                "LOWER_LEFT" in neighbors.keys()
                and "LOWER_RIGHT" in neighbors.keys()
                and isinstance(neighbors["LOWER_LEFT"].state, Empty)
                and isinstance(neighbors["LOWER_RIGHT"].state, Empty)
            ):
                candidates = [
                    neighbors["LOWER_LEFT"],
                    neighbors["LOWER_RIGHT"],
                ]
                n = candidates[randint(0, 1)]
                n_color = n.state._color
                self_color = self.state._color
                ref[n.coord.y][n.coord.x].state = MovableSolid(self_color)
                ref[self.coord.y][self.coord.x].state = Empty(n_color)

            elif "LOWER_LEFT" in neighbors.keys() and isinstance(
                neighbors["LOWER_LEFT"].state, Empty
            ):
                n = neighbors["LOWER_LEFT"]
                n_color = n.state._color
                self_color = self.state._color
                ref[n.coord.y][n.coord.x].state = MovableSolid(self_color)
                ref[self.coord.y][self.coord.x].state = Empty(n_color)

            elif "LOWER_RIGHT" in neighbors.keys() and isinstance(
                neighbors["LOWER_RIGHT"].state, Empty
            ):
                n = neighbors["LOWER_RIGHT"]
                n_color = n.state._color
                self_color = self.state._color
                ref[n.coord.y][n.coord.x].state = MovableSolid(self_color)
                ref[self.coord.y][self.coord.x].state = Empty(n_color)

        self._updated = True
