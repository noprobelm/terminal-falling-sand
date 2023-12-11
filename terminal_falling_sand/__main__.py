import random
from time import sleep
from typing import Optional

from rich.console import Console
from rich.live import Live

from .elements import Sand, Water
from .matrix import CellMatrix


def simulate(
    grid: CellMatrix,
    refresh_per_second: Optional[int] = None,
    render: Optional[bool] = True,
):
    if refresh_per_second is not None:
        refresh_rate = 1 / refresh_per_second
    else:
        refresh_rate = 0

    if render is True:
        with Live(grid, screen=True, auto_refresh=False) as live:
            while True:
                grid.step()
                live.update(grid, refresh=True)
                sleep(refresh_rate)
    else:
        while True:
            grid.step()
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
