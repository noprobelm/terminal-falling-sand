"""Main entrypoint for running the falling sand simulation"""
import random
from time import sleep
from typing import Optional

from rich.console import Console
from rich.live import Live

from .elements import Sand, Water
from .matrix import CellMatrix


def simulate(
    matrix: CellMatrix,
    refresh_per_second: Optional[int] = 60,
    render: Optional[bool] = True,
):
    """Main entrypoint for the simulation

    Takes a cellular matrix as a parameter and runs a simulation from it using the Matrix.step() method.

    Args:
        matrix (CellMatrix): The matrix to run a simulation on
        refresh_per_second (Optional[int]): The refresh rate for the simulation. Set to 'None' to remove rate constraint
        render (Optional[bool]): Whether we should render the simulation to the terminal or not
    """

    if refresh_per_second is not None:
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


def build_grid(xmax: int, ymax: int) -> CellMatrix:
    return CellMatrix(xmax, ymax)


def main():
    console = Console()
    xmax = console.width
    ymax = console.height * 2
    grid = build_grid(console.width, console.height * 2)
    for x in range(xmax // 4, int(xmax * 0.5)):
        for y in range(int(ymax * 0.6), ymax):
            if random.randint(0, 1) == 1:
                grid.spawn(Sand, x, y)

    for x in range(int(xmax * 0.5), int(xmax * 0.75)):
        for y in range(int(ymax * 0.4), int(ymax * 0.6)):
            if random.randint(0, 1) == 1:
                grid.spawn(Sand, x, y)

    for x in range(xmax // 4, int(xmax * 0.5)):
        for y in range(int(ymax * 0.4), int(ymax * 0.6)):
            if random.randint(0, 1) == 1:
                grid.spawn(Water, x, y)

    simulate(grid, 60)


if __name__ == "__main__":
    main()
