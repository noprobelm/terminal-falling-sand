from __future__ import annotations
from random import randint


class State:
    def __init__(self, weight: int):
        self.weight = weight

    def change_state(self, neighbors: dict[str, State]):
        return None


class Empty(State):
    def __init__(self, weight: int):
        self.weight = weight
        pass

    def change_state(self, neighbors: dict):
        return None


class MovableSolid(State):
    def __init__(self, weight: int):
        self.weight = weight

    def change_state(self, neighbors: dict):
        if (
            "LOWER" in neighbors.keys()
            and self.weight > neighbors["LOWER"].state.weight
        ):
            n = neighbors["LOWER"]

        elif (
            "LOWER_LEFT" in neighbors.keys()
            and "LOWER_RIGHT" in neighbors.keys()
            and self.weight > neighbors["LOWER_LEFT"].state.weight
            and self.weight > neighbors["LOWER_RIGHT"].state.weight
        ):
            candidates = [neighbors["LOWER_LEFT"], neighbors["LOWER_RIGHT"]]
            n = candidates[randint(0, 1)]

        elif (
            "LOWER_LEFT" in neighbors.keys()
            and self.weight > neighbors["LOWER_LEFT"].state.weight
        ):
            n = neighbors["LOWER_LEFT"]

        elif (
            "LOWER_RIGHT" in neighbors.keys()
            and self.weight > neighbors["LOWER_RIGHT"].state.weight
        ):
            n = neighbors["LOWER_RIGHT"]
        else:
            return None

        state = n.state

        return (n.coord, state)


class Liquid(State):
    def __init__(self, weight: int):
        self.weight = weight

    def change_state(self, neighbors: dict):
        if (
            "LOWER" in neighbors.keys()
            and self.weight > neighbors["LOWER"].state.weight
        ):
            n = neighbors["LOWER"]

        elif (
            "LOWER_LEFT" in neighbors.keys()
            and "LOWER_RIGHT" in neighbors.keys()
            and self.weight > neighbors["LOWER_LEFT"].state.weight
            and self.weight > neighbors["LOWER_RIGHT"].state.weight
        ):
            candidates = [neighbors["LOWER_LEFT"], neighbors["LOWER_RIGHT"]]
            n = candidates[randint(0, 1)]

        elif (
            "LOWER_LEFT" in neighbors.keys()
            and self.weight > neighbors["LOWER_LEFT"].state.weight
        ):
            n = neighbors["LOWER_LEFT"]

        elif (
            "LOWER_RIGHT" in neighbors.keys()
            and self.weight > neighbors["LOWER_RIGHT"].state.weight
        ):
            n = neighbors["LOWER_RIGHT"]

        elif (
            "LEFT" in neighbors.keys()
            and "RIGHT" in neighbors.keys()
            and self.weight > neighbors["LEFT"].state.weight
            and self.weight > neighbors["RIGHT"].state.weight
        ):
            candidates = [neighbors["LEFT"], neighbors["RIGHT"]]
            n = candidates[randint(0, 1)]

        elif (
            "LEFT" in neighbors.keys() and self.weight > neighbors["LEFT"].state.weight
        ):
            n = neighbors["LEFT"]

        elif "RIGHT" in neighbors.keys() and isinstance(
            neighbors["RIGHT"].state, Empty
        ):
            n = neighbors["RIGHT"]

        else:
            return None

        state = n.state

        return (n.coord, state)
