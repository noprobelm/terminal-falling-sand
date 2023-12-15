"""A module for storing commonly used scenarios"""

import random

from rich.console import Console

from . import elements
from .coordinate import Coordinate
from .simulation import Simulation


def get_console_parameters():
    """Gets the xmax and ymax for the terminal's dimensions"""
    console = Console()
    xmax = console.width
    ymax = console.height * 2
    return (xmax, ymax)


def scenario_1() -> Simulation:
    """Two small hills with some water"""
    xmax, ymax = get_console_parameters()
    sim = Simulation()

    for x in range(xmax // 4, int(xmax * 0.5)):
        for y in range(int(ymax * 0.6), ymax):
            if random.randint(0, 1) == 1:
                c = Coordinate(x, y)
                sim.spawn(elements.Sand, c)

    for x in range(int(xmax * 0.5), int(xmax * 0.75)):
        for y in range(int(ymax * 0.4), int(ymax * 0.6)):
            if random.randint(0, 1) == 1:
                c = Coordinate(x, y)
                sim.spawn(elements.Sand, c)

    for x in range(xmax // 4, int(xmax * 0.5)):
        for y in range(int(ymax * 0.4), int(ymax * 0.6)):
            if random.randint(0, 1) == 1:
                c = Coordinate(x, y)
                sim.spawn(elements.Water, c)

    return sim


def scenario_2() -> Simulation:
    """A single cell of water with one available space for movement"""
    xmax, ymax = get_console_parameters()
    sim = Simulation()
    rock_coords = [
        Coordinate(xmax // 2, ymax - 1),
        Coordinate(xmax // 2 + 3, ymax - 1),
        Coordinate(xmax // 2 + 3, ymax - 1),
    ]
    for c in rock_coords:
        sim.spawn(elements.Rock, c)

    sim.spawn(elements.Water, Coordinate(xmax // 2 + 2, ymax - 1))
    return sim


def scenario_3() -> Simulation:
    """Spawns an hourglass with water flowing down"""
    xmax, ymax = get_console_parameters()
    sim = Simulation(xmax, ymax)

    xmin_left = xmax // 4
    xmax_left = xmax // 2 - 2

    xmax_right = int(xmax * 0.68)

    top = 6
    bottom = ymax

    x = xmin_left
    while x < xmax_left:
        sim.spawn(
            elements.Glass,
            Coordinate(x, bottom - 1),
        )
        sim.spawn(
            elements.Glass,
            Coordinate(x, bottom - 2),
        )

        sim.spawn(
            elements.Glass,
            Coordinate(xmax - x - 2, bottom - 1),
        )
        sim.spawn(
            elements.Glass,
            Coordinate(xmax - x - 2, bottom - 2),
        )

        sim.spawn(
            elements.Glass,
            Coordinate(x, top),
        )
        sim.spawn(
            elements.Glass,
            Coordinate(x, top - 1),
        )

        sim.spawn(
            elements.Glass,
            Coordinate(xmax - x - 2, top),
        )
        sim.spawn(
            elements.Glass,
            Coordinate(xmax - x - 2, top - 1),
        )

        x += 1
        bottom -= 1
        top += 1

    for x in range(xmin_left, xmax_right + 7):
        sim.spawn(elements.Glass, Coordinate(xmax - x - 3, ymax - 1))

    # parameters for water coords
    top = 5
    x_start = xmax // 2 - 34
    x_end = xmax // 2 + 33
    y_start = top
    y_end = ymax // 2 - 5

    # Spawn water at the top of the hourglass
    for y in range(y_start, y_end):
        for x in range(x_start, x_end):
            sim.spawn(elements.Water, Coordinate(x, y))
        x_start += 1
        x_end -= 1

    return sim


SCENARIO_1 = scenario_1()
SCENARIO_2 = scenario_2()
SCENARIO_3 = scenario_3()
