"""CLI entrypoint for running AlphaGrid experiments."""

import logging
from Backend.research.runner.experiment_runner import ExperimentRunner

def main() -> None:

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    runner = ExperimentRunner()  # type: ignore
    runner.run_integration_test()

if __name__ == "__main__":
    main()

