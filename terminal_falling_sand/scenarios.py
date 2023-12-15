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


def scenario_2():
    """A single cell of water with one available space for movement"""
    xmax, ymax = get_console_parameters()
    matrix = CellMatrix(xmax, ymax)
    rock_coords = [
        Coordinate(xmax // 2, ymax - 1),
        Coordinate(xmax // 2 + 3, ymax - 1),
        Coordinate(xmax // 2 + 3, ymax - 1),
    ]
    for c in rock_coords:
        matrix.spawn(elements.Rock, c)

    matrix.spawn(elements.Water, Coordinate(xmax // 2 + 2, ymax - 1))
    return matrix


def scenario_3():
    xmax, ymax = get_console_parameters()
    matrix = CellMatrix(xmax, ymax)

    xmin_left = xmax // 4
    xmax_left = xmax // 2 - 2

    xmax_right = int(xmax * 0.68)

    top = 6
    bottom = ymax

    for y in range(top, top + 10):
        for x in range(xmin_left + 10, xmax_right):
            matrix.spawn(elements.Water, Coordinate(x, y))

    x = xmin_left
    while x < xmax_left:
        matrix.spawn(
            elements.Glass,
            Coordinate(x, bottom - 1),
        )
        matrix.spawn(
            elements.Glass,
            Coordinate(x, bottom - 2),
        )

        matrix.spawn(
            elements.Glass,
            Coordinate(xmax - x - 2, bottom - 1),
        )
        matrix.spawn(
            elements.Glass,
            Coordinate(xmax - x - 2, bottom - 2),
        )

        matrix.spawn(
            elements.Glass,
            Coordinate(x, top),
        )
        matrix.spawn(
            elements.Glass,
            Coordinate(x, top - 1),
        )

        matrix.spawn(
            elements.Glass,
            Coordinate(xmax - x - 2, top),
        )
        matrix.spawn(
            elements.Glass,
            Coordinate(xmax - x - 2, top - 1),
        )

        x += 1
        bottom -= 1
        top += 1

    for x in range(xmin_left, xmax_right + 7):
        matrix.spawn(elements.Glass, Coordinate(xmax - x - 3, ymax - 1))
    # # middle to bottom left
    # y = ymax - 1
    # for x in range(xmax // 4, xmax // 2 - 3):
    #     matrix.spawn(elements.Glass, Coordinate(x, y))
    #     matrix.spawn(elements.Glass, Coordinate(x, y - 1))
    #     y -= 1

    # # middle to top left
    # y = 6
    # for x in range(xmax // 4, xmax // 2 - 3):
    #     matrix.spawn(elements.Glass, Coordinate(x, y))
    #     matrix.spawn(elements.Glass, Coordinate(x, y - 1))
    #     y += 1

    # # middle to bottom right
    # y = ymax // 2 + 3
    # for x in range(xmax // 2 - 1, int(xmax * 0.73) - 1):
    #     matrix.spawn(elements.Glass, Coordinate(x, y))
    #     matrix.spawn(elements.Glass, Coordinate(x, y - 1))
    #     y += 1

    # # middle to top right
    # y = ymax // 2 + 2
    # for x in range(xmax // 2 - 1, int(xmax * 0.73) - 1):
    #     matrix.spawn(elements.Glass, Coordinate(x, y))
    #     matrix.spawn(elements.Glass, Coordinate(x, y - 1))
    #     y -= 1

    # # floor
    # for x in range(xmax // 4, int(xmax * 0.73)):
    #     matrix.spawn(elements.Glass, Coordinate(x, ymax - 1))

    # # sand
    # for x in range(xmax // 4 + 5, int(xmax * 0.73) - 5):
    #     for y in range(4, 10):
    #         matrix.spawn(elements.Sand, Coordinate(x, y))

    return matrix


SCENARIO_1 = scenario_1()
SCENARIO_2 = scenario_2()
SCENARIO_3 = scenario_3()
