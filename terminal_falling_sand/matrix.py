import random
from .cell import Cell, Coordinate
from .cell_state import Empty, MovableSolid
from rich.console import Console, ConsoleOptions
from rich.style import Style
from rich.segment import Segment


class CellMatrix(list):
    def __init__(self, xmax: int, ymax: int) -> None:
        grid = []
        self.max_coord = Coordinate(xmax - 1, ymax - 1)
        self.midpoint = self.max_coord.x // 2
        if self.midpoint % 2 == 1:
            self.midpoint += 1

        for y in range(ymax):
            grid.append([])
            for x in range(xmax):
                c = Coordinate(x, y)
                e = Cell(c, self.max_coord, Empty())
                grid[c.y].append(e)
        super().__init__(grid)

    def fill_random(self, chance: int, rx: range, ry: range) -> None:
        for x in rx:
            for y in ry:
                if random.randint(1, chance) == chance:
                    c = Coordinate(x, y)
                    e = Cell(c, self.max_coord, MovableSolid())
                    self[c.y][c.x] = e

    def step(self):
        for y in range(self.max_coord.y + 1):
            for x1 in range(0, self.midpoint + 1):
                self[self.max_coord.y - y][x1].step(self)
            for x2 in range(self.midpoint, self.max_coord.x + 1):
                self[self.max_coord.y - y][self.max_coord.x - x2 - self.midpoint].step(self)

    def __rich_console__(self, console: Console, options: ConsoleOptions):
        for y in range(self.max_coord.y)[::2]:
            for x in range(self.max_coord.x + 1):
                bg = self[y][x].state._color
                fg = self[y + 1][x].state._color
                yield Segment("▄", Style(color=fg, bgcolor=bg))
            yield Segment.line()
