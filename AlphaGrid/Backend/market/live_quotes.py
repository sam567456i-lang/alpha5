"""Live Quote Engine — fetches live price snapshots with caching fallback."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from Shared.models.market import MarketSnapshot

from .normalizer import DataNormalizer

if TYPE_CHECKING:
    from .connector_manager import ConnectorManager
    from .instruments import InstrumentCatalog

logger = logging.getLogger(__name__)


class LiveQuoteEngine:
    """Orchestrates live quote fetching."""

    def __init__(
        self,
        connector_manager: ConnectorManager,
        instrument_catalog: InstrumentCatalog,
    ) -> None:
        self._manager = connector_manager
        self._catalog = instrument_catalog
        # Simple memory cache: symbol -> MarketSnapshot
        self._cache: dict[str, MarketSnapshot] = {}

    def get_live_quote(self, symbol: str) -> MarketSnapshot | None:
        """Fetch a single live quote."""
        inst = self._catalog.get_by_symbol(symbol)
        exchange = inst.exchange if inst else "NSE"

        try:
            raw_record = self._manager.get_live_quote(symbol, exchange)
            snapshot = DataNormalizer.normalize_live_quote(raw_record)
            self._cache[symbol.upper()] = snapshot
            return snapshot
        except Exception as exc:
            logger.error("Failed to fetch live quote for %s: %s", symbol, exc)
            # Fallback to cache
            cached = self._cache.get(symbol.upper())
            if cached:
                logger.info("Using cached quote for %s", symbol)
                return cached
            return None

    def get_live_quotes(self, symbols: list[str]) -> list[MarketSnapshot]:
        """Fetch a batch of live quotes."""
        if not symbols:
            return []
            
        requests: list[tuple[str, str]] = []
        for sym in symbols:
            inst = self._catalog.get_by_symbol(sym)
            exchange = inst.exchange if inst else "NSE"
            requests.append((sym, exchange))

        try:
            raw_records = self._manager.get_live_quotes(requests)
            snapshots = [DataNormalizer.normalize_live_quote(r) for r in raw_records]
            
            # Update cache
            for s in snapshots:
                self._cache[s.instrument.upper()] = s
                
            return snapshots
        except Exception as exc:
            logger.error("Failed to fetch batch quotes: %s", exc)
            # Fallback to cache for as many as possible
            cached = []
            for sym in symbols:
                c = self._cache.get(sym.upper())
                if c:
                    cached.append(c)
            return cached
