"""Canonical Execution Harness for Provider Layer.

This script bootstraps the AlphaGrid ApplicationContext and attempts
to resolve the required Market Data Providers to natively expose 
missing implementations along the production execution path.
"""

import logging
import sys
import traceback

from Backend.foundation.application_entrypoint import create_application_context
from Backend.market_intelligence.providers.abstract_market_data_provider import HistoricalDataProvider

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("RuntimeAudit")

def main() -> None:
    logger.info("Starting Provider Layer Canonical Pipeline...")
    
    # Bootstrap architecture to ensure DI and Registries are loaded
    logger.info("Bootstrapping ApplicationContext...")
    try:
        app_context = create_application_context()
        logger.info(f"ApplicationContext initialized: {app_context}")
    except Exception as e:
        logger.error(f"Failed to bootstrap architecture: {e}")
        traceback.print_exc()
        sys.exit(1)

    # Attempt to resolve the HistoricalDataProvider
    logger.info("Attempting to resolve HistoricalDataProvider from DI Container...")
    try:
        provider = app_context.container.resolve("historical_data_provider", expected_type=HistoricalDataProvider)
        logger.info(f"SUCCESS: Resolved HistoricalDataProvider: {provider.__class__.__name__}")
        
        # If it magically resolves, try to invoke it to ensure it's not a dummy mock
        logger.info("Attempting to invoke fetch_historical_bars()...")
        # Just passing Nones to see if it immediately crashes with NotImplementedError
        provider.get_historical_bars("AAPL", None, None, "1D") # type: ignore
        
    except Exception as e:
        logger.error(f"RUNTIME CRASH in Provider Layer Pipeline: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
