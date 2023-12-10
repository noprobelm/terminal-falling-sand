from .cell import Cell
from . import cell_state
from .colors import SAND_COLORS
from dataclasses import dataclass


@dataclass
class Element:
    state: cell_state.State
    color: str
