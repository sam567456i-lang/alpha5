"""Canonical Execution Harness for Research Pipeline.

This script bootstraps the AlphaGrid ApplicationContext and executes
the Research Domain's built-in integration tests to organically discover
runtime blockers.
"""

import logging
import sys
import traceback

from Backend.foundation.application_entrypoint import create_application_context
from Backend.research.runner.experiment_runner import ExperimentRunner

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("RuntimeAudit")

def main() -> None:
    logger.info("Starting Research Canonical Pipeline...")
    
    # Bootstrap architecture to ensure DI and Registries are loaded
    logger.info("Bootstrapping ApplicationContext...")
    try:
        app_context = create_application_context()
        logger.info(f"ApplicationContext initialized: {app_context}")
    except Exception as e:
        logger.error(f"Failed to bootstrap architecture: {e}")
        traceback.print_exc()
        sys.exit(1)

    # Initialize the Research Runner
    logger.info("Instantiating ExperimentRunner...")
    try:
        runner = ExperimentRunner()
    except Exception as e:
        logger.error(f"Failed to initialize ExperimentRunner: {e}")
        traceback.print_exc()
        sys.exit(1)

    # Execute the Pipeline
    logger.info("Executing run_integration_test()...")
    try:
        runner.run_integration_test()
        logger.info("Research Pipeline executed successfully (No crashes detected).")
    except Exception as e:
        logger.error(f"RUNTIME CRASH in Research Pipeline: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
