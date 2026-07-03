"""Canonical Execution Harness for Normalization Layer.

This script bootstraps the DI container, resolves the new YFinanceProvider,
fetches real network data, and immediately pipes it into the NormalizationEngine
to organically discover the next implementation gap.
"""

import logging
import sys
import traceback
from datetime import datetime, timedelta, timezone
import pandas as pd

from Backend.foundation.application_entrypoint import create_application_context
from Backend.market_intelligence.providers.abstract_market_data_provider import HistoricalDataProvider
from Backend.market_intelligence.normalization_engine import NormalizationEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("RuntimeAudit")

def print_metadata(df: pd.DataFrame, prefix: str) -> None:
    """Logs formal metadata about a DataFrame without dumping raw contents."""
    if df.empty:
        logger.warning(f"{prefix} DataFrame is empty.")
        return
        
    logger.info(f"{prefix} Row Count: {len(df)}")
    logger.info(f"{prefix} Columns: {list(df.columns)}")
    logger.info(f"{prefix} Dtypes: {df.dtypes.to_dict()}")
    logger.info(f"{prefix} Min Timestamp: {df.index.min()}")
    logger.info(f"{prefix} Max Timestamp: {df.index.max()}")
    logger.info(f"{prefix} Duplicate Indices: {df.index.duplicated().sum()}")
    logger.info(f"{prefix} Null Counts: {df.isnull().sum().to_dict()}")

def main() -> None:
    logger.info("Starting Normalization Layer Canonical Pipeline...")
    
    try:
        app_context = create_application_context()
    except Exception as e:
        logger.error(f"Failed to bootstrap architecture: {e}")
        sys.exit(1)

    try:
        provider = app_context.container.resolve("historical_data_provider", expected_type=HistoricalDataProvider)
        norm_engine = app_context.container.resolve("normalization_engine", expected_type=NormalizationEngine)
    except Exception as e:
        logger.error(f"DI Resolution failed: {e}")
        sys.exit(1)

    # 1. Fetch Raw Data
    symbol = "AAPL"
    timeframe = "1D"
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=30)
    
    logger.info(f"Attempting Provider Execution -> Raw Data Retrieval for {symbol} ({timeframe})")
    try:
        raw_data = provider.get_historical_bars(symbol, start_time, end_time, timeframe)
    except Exception as e:
        logger.error(f"RUNTIME CRASH in Raw Data Retrieval: {e}")
        traceback.print_exc()
        sys.exit(1)

    # Formalize Raw Data Metadata
    logger.info(f"Raw Data Retrieval SUCCESS. Provider ID: {provider.provider_id}, Dataset Version: {provider.dataset_version}")
    print_metadata(raw_data, "RAW_DATA")

    # 2. Normalization Execution
    logger.info("Attempting Normalization Input Boundary...")
    try:
        normalized_data = norm_engine.normalize(raw_data, symbol, timeframe)
    except Exception as e:
        logger.error(f"RUNTIME CRASH in Normalization Engine: {e}")
        traceback.print_exc()
        sys.exit(1)

    # Formalize Normalized Data Metadata
    logger.info("Normalization Execution SUCCESS.")
    print_metadata(normalized_data, "NORMALIZED_DATA")
    
    logger.info("Normalization Layer successfully breached! Frontier advances to Data Quality.")

if __name__ == "__main__":
    main()
