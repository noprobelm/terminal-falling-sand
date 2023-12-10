from . import cell_state
from .cell_state import State
from .colors import SAND_COLORS, WATER_COLORS
from random import randint
from .coordinates import Coordinate
from .cell import Cell


class Element(Cell):
    def __init__(
        self, coord: Coordinate, max_coord: Coordinate, state: State, color: str
    ):
        super().__init__(coord, max_coord, state, color)


class Empty(Element):
    def __init__(self, coord: Coordinate, max_coord: Coordinate):
        state = cell_state.Empty(weight=0)
        color = "black"
        super().__init__(coord, max_coord, state, color)


class Sand(Element):
    def __init__(self, coord: Coordinate, max_coord: Coordinate):
        state = cell_state.MovableSolid(weight=2)
        color = SAND_COLORS[randint(0, len(SAND_COLORS) - 1)]
        super().__init__(coord, max_coord, state, color)


class Water(Element):
    def __init__(self, coord: Coordinate, max_coord: Coordinate):
        state = cell_state.Liquid(weight=1)
        color = WATER_COLORS[randint(0, len(WATER_COLORS) - 1)]
        super().__init__(coord, max_coord, state, color)
