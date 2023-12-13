"""A module for storing commonly used scenarios"""

import random

from rich.console import Console

from . import elements
from .coordinate import Coordinate
from .matrix import CellMatrix


def get_console_parameters():
    """Gets the xmax and ymax for the terminal's dimensions"""
    console = Console()
    xmax = console.width
    ymax = console.height * 2
    return (xmax, ymax)


def scenario_1():
    """Two small hills with some water"""

    xmax, ymax = get_console_parameters()
    matrix = CellMatrix(xmax, ymax)

    for x in range(xmax // 4, int(xmax * 0.5)):
        for y in range(int(ymax * 0.6), ymax):
            if random.randint(0, 1) == 1:
                c = Coordinate(x, y)
                matrix.spawn(elements.Sand, c)

    for x in range(int(xmax * 0.5), int(xmax * 0.75)):
        for y in range(int(ymax * 0.4), int(ymax * 0.6)):
            if random.randint(0, 1) == 1:
                c = Coordinate(x, y)
                matrix.spawn(elements.Sand, c)

    for x in range(xmax // 4, int(xmax * 0.5)):
        for y in range(int(ymax * 0.4), int(ymax * 0.6)):
            if random.randint(0, 1) == 1:
                c = Coordinate(x, y)
                matrix.spawn(elements.Water, c)

    return matrix


SCENARIO_1 = scenario_1()