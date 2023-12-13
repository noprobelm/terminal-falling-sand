from rich.live import Live
from rich.console import Console
from typing import Optional, Union
from .matrix import CellMatrix
from time import sleep
from .coordinate import Coordinate
from .elements import Sand, Water
import random


class Simulation:
    def __init__(self):
        console = Console()
        xmax = console.width
        ymax = console.height * 2
        self.matrix = CellMatrix(xmax, ymax)

        for x in range(xmax // 4, int(xmax * 0.5)):
            for y in range(int(ymax * 0.6), ymax):
                if random.randint(0, 1) == 1:
                    c = Coordinate(x, y)
                    self.matrix.spawn(Sand, c)

        for x in range(int(xmax * 0.5), int(xmax * 0.75)):
            for y in range(int(ymax * 0.4), int(ymax * 0.6)):
                if random.randint(0, 1) == 1:
                    c = Coordinate(x, y)
                    self.matrix.spawn(Sand, c)

        for x in range(xmax // 4, int(xmax * 0.5)):
            for y in range(int(ymax * 0.4), int(ymax * 0.6)):
                if random.randint(0, 1) == 1:
                    c = Coordinate(x, y)
                    self.matrix.spawn(Water, c)

    def start(
        self,
        duration: Union[float, int] = 0,
        fps: int = 60,
        render: Optional[bool] = True,
        debug=False,
    ):
        if fps > 0:
            refresh_rate = 1 / fps
            print(refresh_rate)
        else:
            refresh_rate = fps

        if duration == 0:
            duration = float("inf")

        if debug is True:
            import cProfile

            cProfile.runctx(
                "exec(self.run(duration, refresh_rate, False))", globals(), locals()
            )

        elif render is True:
            self.run(duration, refresh_rate, True)

        else:
            self.run(duration, refresh_rate, False)

    def run(
        self,
        duration: Union[float, int],
        refresh_rate: Union[float, int],
        render: bool,
    ):
        elapsed = 0
        if render is True:
            with Live(self.matrix, screen=True, auto_refresh=False) as live:
                while elapsed < duration:
                    self.matrix.step()
                    live.update(self.matrix, refresh=True)
                    sleep(refresh_rate)
                    elapsed += 1
        else:
            while elapsed < duration:
                self.matrix.step()
                sleep(refresh_rate)
                elapsed += 1
