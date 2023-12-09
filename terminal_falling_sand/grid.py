import random
from .element import Element, Coordinate
from .state import State, Empty, MovableSolid
from enum import Enum
from rich.console import Console, ConsoleOptions
from rich.table import Table
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from rich.style import Style
from rich.segment import Segment


class MooreNeighborhood(Enum):
    UPPER_LEFT = (-1, -1)
    UPPER = (0, -1)
    UPPER_RIGHT = (1, -1)
    RIGHT = (1, 0)
    LOWER_RIGHT = (1, 1)
    LOWER = (0, 1)
    LOWER_LEFT = (-1, 1)
    LEFT = (-1, 0)


class GridList(list):
    def __init__(self, xmax: int, ymax: int) -> None:
        grid = []
        self.xmax = xmax - 1
        self.ymax = ymax - 1
        for y in range(ymax):
            grid.append([])
            for x in range(xmax):
                c = Coordinate(x, y)
                e = Element(c, Empty(), xmax - 1, ymax - 1)
                grid[c.y].append(e)
        super().__init__(grid)

    def fill_random(self, chance: int, rx: range, ry: range) -> None:
        for x in rx:
            for y in ry:
                if random.randint(1, chance) == chance:
                    c = Coordinate(x, y)
                    e = Element(c, MovableSolid(), self.xmax, self.ymax)
                    self[c.y][c.x] = e

    def step(self):
        for y in range(self.ymax + 1):
            for x in range(self.xmax + 1):
                self[self.ymax - y][self.xmax - x].step(self)

        for y in range(self.ymax + 1):
            for x in range(self.xmax + 1):
                self[y][x]._updated = False

    def __rich_console__(self, console: Console, options: ConsoleOptions):
        for y in range(self.ymax)[::2]:
            for x in range(self.xmax + 1):
                bg = self[y][x].state._color
                fg = self[y + 1][x].state._color
                yield Segment("▄", Style(color=fg, bgcolor=bg))
            yield Segment.line()


"""
        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = {
                executor.submit(self.update_element, ref, element): element
                for element in flattened
            }

            for future in concurrent.futures.as_completed(futures):
                new = future.result()
                self[new[0].y][new[0].x].state = new[1]

"""
