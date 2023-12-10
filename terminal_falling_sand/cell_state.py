from __future__ import annotations
from random import randint
from .coordinates import Coordinate


class State:
    def __init__(self):
        pass

    def change_state(self, neighbors: dict[str, State]):
        return None


class Empty(State):
    def __init__(self):
        pass

    def change_state(self, neighbors: dict):
        return None


class MovableSolid(State):
    def __init__(self):
        pass

    def change_state(self, neighbors: dict):
        if "LOWER" in neighbors.keys() and isinstance(neighbors["LOWER"].state, Empty):
            n = neighbors["LOWER"]

        elif (
            "LOWER_LEFT" in neighbors.keys()
            and "LOWER_RIGHT" in neighbors.keys()
            and isinstance(neighbors["LOWER_LEFT"].state, Empty)
            and isinstance(neighbors["LOWER_RIGHT"].state, Empty)
        ):
            candidates = [neighbors["LOWER_LEFT"], neighbors["LOWER_RIGHT"]]
            n = candidates[randint(0, 1)]

        elif "LOWER_LEFT" in neighbors.keys() and isinstance(
            neighbors["LOWER_LEFT"].state, Empty
        ):
            n = neighbors["LOWER_LEFT"]

        elif "LOWER_RIGHT" in neighbors.keys() and isinstance(
            neighbors["LOWER_RIGHT"].state, Empty
        ):
            n = neighbors["LOWER_RIGHT"]
        else:
            return None

        state = n.state

        return (n.coord, state)


class Liquid(State):
    def __init__(self):
        pass

    def change_state(self, neighbors: dict):
        if "LOWER" in neighbors.keys() and isinstance(neighbors["LOWER"].state, Empty):
            n = neighbors["LOWER"]

        elif (
            "LOWER_LEFT" in neighbors.keys()
            and "LOWER_RIGHT" in neighbors.keys()
            and isinstance(neighbors["LOWER_LEFT"].state, Empty)
            and isinstance(neighbors["LOWER_RIGHT"].state, Empty)
        ):
            candidates = [neighbors["LOWER_LEFT"], neighbors["LOWER_RIGHT"]]
            n = candidates[randint(0, 1)]

        elif "LOWER_LEFT" in neighbors.keys() and isinstance(
            neighbors["LOWER_LEFT"].state, Empty
        ):
            n = neighbors["LOWER_LEFT"]

        elif "LOWER_RIGHT" in neighbors.keys() and isinstance(
            neighbors["LOWER_RIGHT"].state, Empty
        ):
            n = neighbors["LOWER_RIGHT"]

        elif (
            "LEFT" in neighbors.keys()
            and "RIGHT" in neighbors.keys()
            and isinstance(neighbors["LEFT"].state, Empty)
            and isinstance(neighbors["RIGHT"].state, Empty)
        ):
            candidates = [neighbors["LOWER_LEFT"], neighbors["LOWER_RIGHT"]]
            n = candidates[randint(0, 1)]

        elif "LEFT" in neighbors.keys() and isinstance(neighbors["LEFT"].state, Empty):
            n = neighbors["LEFT"]

        elif "RIGHT" in neighbors.keys() and isinstance(
            neighbors["RIGHT"].state, Empty
        ):
            n = neighbors["RIGHT"]

        else:
            return None

        state = n.state

        return (n.coord, state)
