from __future__ import annotations

from time import sleep
from typing import Optional, Union

from rich.console import Console
from rich.live import Live

from .matrix import CellMatrix


class Simulation:
    """A class to run a simulation from the terminal

    Default behavior is to run the simulation at the current dimensions of the terminal. Currently, this is not
    modifiable by the user without direct interference with the underlying matrix attr

    Attributes:
        1. matrix (CellMatrix): The underlying cell matrix
    """

    def __init__(self, matrix: Optional[CellMatrix] = None) -> None:
        """Initializes an instance of the Simulation class"""

        console = Console()
        xmax = console.width
        ymax = console.height * 2
        self.matrix = matrix or CellMatrix(xmax, ymax)

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
            sleep_for = 0
        else:
            sleep_for = 1 / refresh_rate

        if duration == 0:
            duration = float("inf")

        if debug is True:
            import cProfile

            cProfile.runctx(
                "exec(self.run(duration, sleep_for, False))", globals(), locals()
            )

        elif render is True:
            self.run(duration, sleep_for, True)

        else:
            self.run(duration, sleep_for, False)

    def run(
        self,
        duration: Union[float, int],
        sleep_for: Union[float, int],
        render: bool,
    ) -> None:
        """Runs the simulation

        Args:
            duration (Union[float, int]): The duration the simulation should run for
            sleep_for (Union[float, int]): The time the simulation should sleep between each step
            render: bool: Cotnrols if the simulation renders to the terminal
        """
        elapsed = 0
        if render is True:
            with Live(self.matrix, screen=True, auto_refresh=False) as live:
                while elapsed < duration:
                    self.matrix.step()
                    live.update(self.matrix, refresh=True)
                    sleep(sleep_for)
                    elapsed += 1
        else:
            while elapsed < duration:
                self.matrix.step()
                sleep(sleep_for)
                elapsed += 1

    @classmethod
    def from_matrix(cls, matrix: CellMatrix) -> Simulation:
        return cls(matrix)
