"""Main entrypoint for running the falling sand simulation"""

import random
from time import sleep
from typing import Optional

from rich.console import Console
from rich.live import Live

from .coordinate import Coordinate
from .elements import Sand, Water, Rock
from .matrix import CellMatrix


def simulate(
    matrix: CellMatrix,
    refresh_per_second: int = 60,
    render: Optional[bool] = True,
) -> None:
    """Main entrypoint for the simulation

    Takes a cellular matrix as a parameter and runs a simulation from it using the Matrix.step() method.

    Args:
        matrix (CellMatrix): The matrix to run a simulation on
        refresh_per_second (Optional[int]): The refresh rate for the simulation. Set to 'None' to remove rate constraint
        render (Optional[bool]): Whether we should render the simulation to the terminal or not

    """
    if refresh_per_second > 0:
        refresh_rate = 1 / refresh_per_second
    else:
        refresh_rate = 0

    if render is True:
        with Live(matrix, screen=True, auto_refresh=False) as live:
            while True:
                matrix.step()
                live.update(matrix, refresh=True)
                sleep(refresh_rate)
    else:
        while True:
            matrix.step()
            sleep(refresh_rate)


def build_matrix(xmax: int, ymax: int) -> CellMatrix:
    """Builds a grid based on x and y constraints

    Args:
        xmax (int): The maximum x value for the grid
        ymax (int): The maximum y value for the grid

    Note
        If rendering to a terminal, ymax might be best to set to twice the terminal's height. This is to accommodate
        the height/width aspect ratio of ASCII text in the terminal (which is usually 2:1).

    Returns:
        CellMatrix

    """
    return CellMatrix(xmax, ymax)


def main() -> None:
    """Main entrypoint for setting grid parameters and spawning elements into the simulation

    - Sets an xmax/ymax based on the invoking terminal's dimensions, then builds a grid based on these values.
    - Spawns in various elements to participate in the simulation
    - Runs the simulate method using default args

    """
    console = Console()
    xmax = console.width
    ymax = console.height * 2
    grid = build_matrix(console.width, console.height * 2)
    for x in range(xmax // 4, int(xmax * 0.5)):
        for y in range(int(ymax * 0.6), ymax):
            if random.randint(0, 1) == 1:
                c = Coordinate(x, y)
                grid.spawn(Sand, c)

    for x in range(int(xmax * 0.5), int(xmax * 0.75)):
        for y in range(int(ymax * 0.4), int(ymax * 0.6)):
            if random.randint(0, 1) == 1:
                c = Coordinate(x, y)
                grid.spawn(Sand, c)

    for x in range(xmax // 4, int(xmax * 0.5)):
        for y in range(int(ymax * 0.4), int(ymax * 0.6)):
            if random.randint(0, 1) == 1:
                c = Coordinate(x, y)
                grid.spawn(Water, c)


if __name__ == "__main__":
    main()
