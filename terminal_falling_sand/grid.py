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
    def __init__(self, x_max: int, y_max: int) -> None:
        grid = []
        self._x_max = x_max - 1
        self._y_max = y_max - 1
        for y in range(y_max):
            grid.append([])
            for x in range(x_max):
                c = Coordinate(x, y)
                e = Element(c, Empty())
                grid[c.y].append(e)
        super().__init__(grid)

    def fill_random(self, chance: int, rx: range, ry: range) -> None:
        for x in rx:
            for y in ry:
                if random.randint(1, chance) == chance:
                    c = Coordinate(x, y)
                    e = Element(c, MovableSolid())
                    self[c.y][c.x] = e

    def step(self):
        elements = []
        for y in range(self._y_max):
            elements.extend([self[y][x] for x in range(self._x_max)])

        for element in elements:
            self.update_element(element)

    def update_element(self, element):
        element.step(self)

    def __rich_console__(self, console: Console, options: ConsoleOptions):
        for y in range(self._y_max)[::2]:
            for x in range(self._x_max + 1):
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
