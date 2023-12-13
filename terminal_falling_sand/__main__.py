"""Main entrypoint for running the falling sand simulation"""

from .simulation import Simulation


def main() -> None:
    """Main entrypoint for running a simulation on default settings"""
    sim = Simulation()
    sim.start(render=True)


if __name__ == "__main__":
    main()
