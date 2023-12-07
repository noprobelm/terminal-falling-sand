from .grid import Grid
from enum import Enum
from rich.console import Console
from rich.live import Live
from time import sleep


class Neighbors(Enum):
    UPPER = (0, -1)
    UPPER_RIGHT = (1, -1)
    RIGHT = ((1, 0),)
    LOWER_RIGHT = (1, 1)
    LOWER = (0, 1)
    LOWER_LEFT = (-1, 1)
    LEFT = (-1, 0)
    UPPER_LEFT = (-1, -1)


def main():
    console = Console()
    x_max = console.width
    y_max = console.height * 2
    grid = Grid(x_max, y_max)
    grid.fill_random(2, range(0, x_max), range(0, y_max // 6))
    with Live(grid, console=console, screen=True, auto_refresh=False) as live:
        while True:
            grid.step()
            live.update(grid, refresh=True)


if __name__ == "__main__":
    main()
