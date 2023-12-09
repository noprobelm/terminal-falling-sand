from .grid import Grid
from rich.console import Console
from rich.live import Live
from time import sleep
from typing import Optional


def terminal_render(grid: Grid, refresh_per_second: Optional[int] = None):
    if refresh_per_second is not None:
        refresh_rate = 1 / refresh_per_second
    else:
        refresh_rate = 0
    with Live(grid, screen=True, auto_refresh=False) as live:
        while True:
            grid.step()
            live.update(grid, refresh=True)
            sleep(refresh_rate)


def build_grid(xmax: int, ymax: int) -> Grid:
    return Grid(xmax, ymax)


def main():
    console = Console()
    xmax = console.width
    ymax = console.height * 2
    grid = build_grid(console.width, console.height * 2)
    grid.fill_random(2, range(xmax // 4, int(xmax * 0.75)), range(ymax))

    terminal_render(grid, 60)


if __name__ == "__main__":
    main()
