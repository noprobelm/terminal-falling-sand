"""Main entrypoint for running the falling sand simulation"""

from .simulation import Simulation
from .scenarios import SCENARIO_1


def main() -> None:
    """Main entrypoint for running a simulation on default settings"""
    sim = Simulation.from_matrix(SCENARIO_1)
    sim.start(60)


if __name__ == "__main__":
    main()
