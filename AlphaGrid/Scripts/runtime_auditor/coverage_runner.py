import json
import logging
import os
import sys
import unittest
from typing import Optional

try:
    import coverage
except ImportError:
    coverage = None

from Scripts.runtime_auditor.instrumentation import AuditorInstrumentor, InstrumentationContext

logger = logging.getLogger("RuntimeAuditor.CoverageRunner")
logging.basicConfig(level=logging.INFO)

def run_tests_with_coverage(output_dir: str):
    """Executes all unit tests with coverage to capture the execution graph."""
    if not coverage:
        logger.error("The 'coverage' package is not installed. Run: pip install coverage")
        sys.exit(1)

    cov = coverage.Coverage(
        data_file=os.path.join(output_dir, ".coverage"),
        source=["Backend"],
        omit=["Backend/tests/*", "*/__pycache__/*", "*/site-packages/*"]
    )
    cov.start()

    # Apply instrumentation
    instrumentor = AuditorInstrumentor()
    instrumentor.apply()

    try:
        # Discover and run tests (E2E simulation)
        loader = unittest.TestLoader()
        # We start at the top of Tests/ or Backend/tests
        suite = loader.discover(start_dir="Tests")
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
        
        # Also run backend tests if any remain
        suite2 = loader.discover(start_dir="Backend/tests")
        runner.run(suite2)

    finally:
        instrumentor.remove()
        cov.stop()
        cov.save()
        
        # Dump instrumentation data
        InstrumentationContext.dump_to_disk(output_dir)

        # Generate JSON coverage report
        cov.json_report(outfile=os.path.join(output_dir, "coverage.json"))
        logger.info(f"Coverage and Instrumentation graphs saved to {output_dir}")

if __name__ == "__main__":
    output_directory = os.path.join(os.path.dirname(__file__), "output")
    run_tests_with_coverage(output_directory)
