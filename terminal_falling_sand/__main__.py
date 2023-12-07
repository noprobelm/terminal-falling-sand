from .grid import GridDict, GridList
from rich.console import Console
from rich.live import Live
from time import sleep


def main():
    console = Console()
    x_max = console.width
    y_max = console.height
    grid = GridDict(x_max, y_max)
    grid.fill_random(2, range(0, x_max), range(0, y_max // 6))
    with Live(grid, console=console, screen=True, auto_refresh=False) as live:
        while True:
            grid.step()
            live.update(grid, refresh=True)


if __name__ == "__main__":
    main()
