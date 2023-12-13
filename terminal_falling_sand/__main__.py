"""Main entrypoint for running the falling sand simulation"""

from .simulation import Simulation
from . import scenarios
from .args import args


def main() -> None:
    """Main entrypoint for running a simulation on default settings"""
    sim = Simulation.from_matrix(scenarios.SCENARIO_1)
    sim.start(**args)


if __name__ == "__main__":
    main()
