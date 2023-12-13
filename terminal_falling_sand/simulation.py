import random
from time import sleep
from typing import Optional, Union

from rich.console import Console
from rich.live import Live

from .coordinate import Coordinate
from .elements import Sand, Water
from .matrix import CellMatrix


class Simulation:
    """A class to run a simulation from the terminal

    Default behavior is to run the simulation at the current dimensions of the terminal. Currently, this is not
    modifiable by the user without direct interference with the underlying matrix attr

    Attributes:
        1. matrix (CellMatrix): The underlying cell matrix
    """

    def __init__(self) -> None:
        """Initializes an instance of the Simulation class"""

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
        refresh_rate: Optional[int] = None,
        duration: Union[float, int] = 0,
        render: Optional[bool] = True,
        debug=False,
    ) -> None:
        """Sets initial parameters for the simluation, then runs it

        Args:
            duration (Union[float, int]): The duration the simulation should run for. Defaults to 0 (infinity)
            refresh_rate (int): The number of times the simluation should run before sleeping. Defaults to None
            render (bool): Controls if the simulation renders to the terminal. Defaults to True
            debug (bool): Controls if the simulation runs in debug mode. This will run cProfile and disable rendering
        """
        if refresh_rate is None:
            sleep_time = 0
        else:
            sleep_time = 1 / refresh_rate

        if duration == 0:
            duration = float("inf")

        if debug is True:
            import cProfile

            cProfile.runctx(
                "exec(self.run(duration, refresh_rate, False))", globals(), locals()
            )

        elif render is True:
            self.run(duration, sleep_time, True)

        else:
            self.run(duration, sleep_time, False)

    def run(
        self,
        duration: Union[float, int],
        sleep_time: Union[float, int],
        render: bool,
    ) -> None:
        """Runs the simulation

        Args:
            duration (Union[float, int]): The duration the simulation should run for
            sleep_time (Union[float, int]): The time the simulation should sleep between each step
            render: bool: Cotnrols if the simulation renders to the terminal
        """
        elapsed = 0
        if render is True:
            with Live(self.matrix, screen=True, auto_refresh=False) as live:
                while elapsed < duration:
                    self.matrix.step()
                    live.update(self.matrix, refresh=True)
                    sleep(sleep_time)
                    elapsed += 1
        else:
            while elapsed < duration:
                self.matrix.step()
                sleep(sleep_time)
                elapsed += 1
