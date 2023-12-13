"""Main entrypoint for running the falling sand simulation"""

import random
from time import sleep
from typing import Optional
from .simulation import Simulation
from rich.console import Console
from rich.live import Live

from .coordinate import Coordinate
from .elements import Sand, Water
from .matrix import CellMatrix


def build_matrix(xmax: int, ymax: int) -> CellMatrix:
    """Builds a matrix based on x and y constraints

    Args:
        xmax (int): The maximum x value for the matrix
        ymax (int): The maximum y value for the matrix

    Note
        If rendering to a terminal, ymax might be best to set to twice the terminal's height. This is to accommodate
        the height/width aspect ratio of ASCII text in the terminal (which is usually 2:1).

    Returns:
        CellMatrix

    """
    return CellMatrix(xmax, ymax)


def main() -> None:
    """Main entrypoint for setting matrix parameters and spawning elements into the simulation

    - Sets an xmax/ymax based on the invoking terminal's dimensions, then builds a matrix based on these values.
    - Spawns in various elements to participate in the simulation
    - Runs the simulate method using default args

    """
    sim = Simulation()
    sim.start(render=True)


if __name__ == "__main__":
    main()
