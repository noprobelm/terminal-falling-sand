import random
from .element import Element, MovableSolid, Coordinate, Empty
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


class GridDict(dict):
    def __init__(self, x_max: int, y_max: int) -> None:
        self._x_max = x_max - 1
        self._y_max = y_max - 1
        grid = {}
        for i in range(x_max):
            for k in range(y_max):
                c = Coordinate(i, k)
                grid[c] = Empty(c)
        super().__init__(grid)

    def fill_random(self, chance: int, rx: range, ry: range) -> None:
        for x in rx:
            for y in ry:
                if random.randint(1, chance) == chance:
                    c = Coordinate(x, y)
                    self[c] = MovableSolid(c)

    def _neighbors(self, c: Coordinate) -> dict[str, Element]:
        neighbors = {}
        for n in MooreNeighborhood:
            nc = c + Coordinate(*n.value)
            if nc.x >= 0 and nc.x <= self._x_max and nc.y >= 0 and nc.y <= self._y_max:
                neighbors[n.name] = self[nc]
        return neighbors

    def step(self):
        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = {
                executor.submit(self.update_element, coord, element): coord
                for coord, element in self.items()
            }

            for future in concurrent.futures.as_completed(futures):
                new = future.result()
                if new is not None:
                    self.update(new)

    def update_element(self, coord, element):
        if isinstance(element, Empty):
            return
        neighbors = self._neighbors(coord)
        if all(
            [
                isinstance(neighbors.get(n), MovableSolid)
                for n in ["LOWER", "LOWER_LEFT", "LOWER_RIGHT"]
            ]
        ):
            return
        new = element.step(neighbors)
        return new

    def __rich_console__(self, console: Console, options: ConsoleOptions):
        for y in range(self._y_max)[::2]:
            for x in range(self._x_max + 1):
                bg = self[Coordinate(x, y)]._color
                fg = self[Coordinate(x, y + 1)]._color
                yield Segment("▄", Style(color=fg, bgcolor=bg))
            yield Segment.line()


class GridList(list):
    def __init__(self, x_max: int, y_max: int) -> None:
        self._x_max = x_max - 1
        self._y_max = y_max - 1
        grid = []
        for y in range(y_max):
            grid.append([])
            for x in range(x_max):
                c = Coordinate(x, y)
                grid[c.y].append(Empty(c))
        super().__init__(grid)

    def fill_random(self, chance: int, rx: range, ry: range) -> None:
        for x in rx:
            for y in ry:
                if random.randint(1, chance) == chance:
                    c = Coordinate(x, y)
                    self[c.y][c.x] = MovableSolid(c)

    def _neighbors(self, c: Coordinate) -> dict[str, Element]:
        neighbors = {}
        for n in MooreNeighborhood:
            nc = c + Coordinate(*n.value)
            if nc.x >= 0 and nc.x <= self._x_max and nc.y >= 0 and nc.y <= self._y_max:
                neighbors[n.name] = self[nc.y][nc.x]
        return neighbors

    def update_element(self, element):
        if isinstance(element, Empty):
            return
        neighbors = self._neighbors(element.coordinate)
        if all(
            [
                isinstance(neighbors.get(n), MovableSolid)
                for n in ["LOWER", "LOWER_LEFT", "LOWER_RIGHT"]
            ]
        ):
            return
        new = element.step(neighbors)
        return new

    def step(self):
        with ThreadPoolExecutor(max_workers=16) as executor:
            flattened = []
            for row in self:
                flattened.extend(row)
            futures = {
                executor.submit(self.update_element, element): element
                for element in flattened
            }

            for future in concurrent.futures.as_completed(futures):
                new = future.result()
                if new:
                    for n in new:
                        self[n.y][n.x] = new[n]

    def __rich_console__(self, console: Console, options: ConsoleOptions):
        for y in range(self._y_max)[::2]:
            for x in range(self._x_max + 1):
                bg = self[y][x]._color
                fg = self[y + 1][x]._color
                yield Segment("▄", Style(color=fg, bgcolor=bg))
            yield Segment.line()
