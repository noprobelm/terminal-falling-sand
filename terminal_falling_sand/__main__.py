from .grid import GridList
from rich.console import Console
from rich.live import Live
from time import sleep


def main():
    console = Console()
    x_max = console.width
    y_max = console.height * 2
    grid = GridList(x_max, y_max)
    grid.fill_random(2, range(x_max // 4, int(x_max * 0.75)), range(y_max // 2))

    with Live(grid, console=console, screen=True, auto_refresh=False) as live:
        while True:
            grid.step()
            live.update(grid, refresh=True)


if __name__ == "__main__":
    main()
