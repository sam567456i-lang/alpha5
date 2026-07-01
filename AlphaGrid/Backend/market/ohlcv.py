"""Historical OHLCV Engine — fetches, validates, and normalizes candlestick data."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING

from Shared.models.market import MarketSnapshot

from .normalizer import DataNormalizer
from .validator import OHLCVValidator

if TYPE_CHECKING:
    from .connector_manager import ConnectorManager
    from .instruments import InstrumentCatalog

logger = logging.getLogger(__name__)


class OHLCVEngine:
    """Orchestrates historical candle fetching."""

    def __init__(
        self,
        connector_manager: ConnectorManager,
        instrument_catalog: InstrumentCatalog,
    ) -> None:
        self._manager = connector_manager
        self._catalog = instrument_catalog

    def get_ohlcv(
        self,
        symbol: str,
        timeframe: str,
        from_dt: datetime,
        to_dt: datetime,
    ) -> list[MarketSnapshot]:
        """Fetch historical OHLCV data for a given symbol and timeframe.

        Flow:
        1. Look up exchange in catalog.
        2. Fetch raw records via ConnectorManager (with failover).
        3. Validate records (drop bad ones).
        4. Normalize to Shared MarketSnapshot DTOs.
        """
        inst = self._catalog.get_by_symbol(symbol)
        exchange = inst.exchange if inst else "NSE"

        try:
            # 1. Fetch raw data
            raw_records = self._manager.get_ohlcv(
                symbol=symbol,
                exchange=exchange,
                timeframe=timeframe,
                from_dt=from_dt,
                to_dt=to_dt,
            )
        except Exception as exc:
            logger.error("Failed to fetch OHLCV for %s: %s", symbol, exc)
            return []

        # 2. Validate
        valid_records = OHLCVValidator.validate_all(raw_records)
        
        if len(valid_records) < len(raw_records):
            logger.warning(
                "Dropped %d invalid records for %s", 
                len(raw_records) - len(valid_records), symbol
            )

        # 3. Normalize
        snapshots = [DataNormalizer.normalize_ohlcv(r) for r in valid_records]

        # 4. Return sorted by timestamp
        snapshots.sort(key=lambda s: s.timestamp)
        return snapshots
