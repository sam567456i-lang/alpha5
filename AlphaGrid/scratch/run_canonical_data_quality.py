"""Canonical Execution Harness for Data Quality Layer.

This script organically pipes data from the Normalization Layer into the
Data Quality Gate to formally expose the next implementation gap in the sequence.
"""

import logging
import sys
import traceback
from datetime import datetime, timedelta, timezone

from Backend.foundation.application_entrypoint import create_application_context
from Backend.market_intelligence.providers.abstract_market_data_provider import HistoricalDataProvider
from Backend.market_intelligence.normalization_engine import NormalizationEngine
from Backend.market_intelligence.data_quality_gate import DataQualityGate
from Backend.market_intelligence.session_engine import SessionEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("RuntimeAudit")

def main() -> None:
    logger.info("Starting Data Quality Layer Canonical Pipeline...")
    
    try:
        app_context = create_application_context()
    except Exception as e:
        logger.error(f"Failed to bootstrap architecture: {e}")
        sys.exit(1)

    try:
        provider = app_context.container.resolve("historical_data_provider", expected_type=HistoricalDataProvider)
        norm_engine = app_context.container.resolve("normalization_engine", expected_type=NormalizationEngine)
        session_engine = app_context.container.resolve("session_engine", expected_type=SessionEngine)
    except Exception as e:
        logger.error(f"Upstream DI Resolution failed: {e}")
        sys.exit(1)

    # 1. Attempt Data Quality Gate Resolution
    logger.info("Attempting to resolve DataQualityGate from DI Container...")
    try:
        dq_gate = app_context.container.resolve("data_quality_gate", expected_type=DataQualityGate)
        logger.info("DataQualityGate resolved successfully.")
    except Exception as e:
        logger.error(f"RUNTIME CRASH in DI Resolution: {e}")
        traceback.print_exc()
        sys.exit(1)

    # 2. Upstream Execution
    symbol = "AAPL"
    timeframe = "1D"
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=30)
    
    logger.info("Executing upstream pipeline...")
    raw_data = provider.get_historical_bars(symbol, start_time, end_time, timeframe)
    normalized_data = norm_engine.normalize(raw_data, symbol, timeframe)
    
    # 3. Calculate Expected Bars
    logger.info("Attempting to calculate expected_bars from SessionEngine...")
    try:
        # We enforce calling the SessionEngine because the protocol mandates Reality-Only parameters
        expected_bars = session_engine.calculate_expected_bars(start_time, end_time, timeframe)
    except AttributeError as e:
        logger.error(f"RUNTIME CRASH in SessionEngine logic: {e}")
        traceback.print_exc()
        sys.exit(1)

    # 4. Data Quality Gate Execution
    logger.info("Executing DataQualityGate...")
    try:
        accepted = dq_gate.evaluate_and_enforce(normalized_data, expected_bars, symbol)
        logger.info(f"Data Quality Gate result: Accepted={accepted}")
    except Exception as e:
        logger.error(f"RUNTIME CRASH in DataQualityGate logic: {e}")
        traceback.print_exc()
        sys.exit(1)

    logger.info("Data Quality Layer successfully breached!")

if __name__ == "__main__":
    main()
