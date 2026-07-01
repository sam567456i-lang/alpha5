"""Instrument Catalog — manages the master list of tradable instruments."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .normalizer import DataNormalizer

if TYPE_CHECKING:
    from .connector_manager import ConnectorManager
    from .providers.base import InstrumentRecord

logger = logging.getLogger(__name__)


class InstrumentCatalog:
    """Provides access to the instrument master list.
    
    Caches the list in memory after the first fetch from the ConnectorManager.
    """

    def __init__(self, connector_manager: ConnectorManager) -> None:
        self._manager = connector_manager
        self._cache: list[InstrumentRecord] | None = None
        self._symbol_map: dict[str, InstrumentRecord] = {}

    def _ensure_loaded(self) -> None:
        if self._cache is not None:
            return

        try:
            raw_instruments = self._manager.get_instruments()
            self._cache = []
            
            for inst in raw_instruments:
                # Normalize the symbol and exchange before caching
                norm_sym = DataNormalizer._normalize_symbol(inst.symbol)
                norm_exch = DataNormalizer._normalize_exchange(inst.exchange)
                
                # We mutate a copy for the cache
                from dataclasses import replace
                cached_inst = replace(inst, symbol=norm_sym, exchange=norm_exch)
                
                self._cache.append(cached_inst)
                self._symbol_map[norm_sym] = cached_inst
                
            logger.info("Loaded %d instruments into catalog cache.", len(self._cache))
        except Exception as exc:
            logger.error("Failed to load instrument catalog: %s", exc)
            self._cache = []
            self._symbol_map = {}

    def get_all(
        self, exchange: str | None = None, segment: str | None = None
    ) -> list[InstrumentRecord]:
        """Return all instruments, optionally filtered by exchange and/or segment."""
        self._ensure_loaded()
        assert self._cache is not None
        
        results = self._cache
        if exchange:
            ex = exchange.upper()
            results = [r for r in results if r.exchange == ex]
        if segment:
            seg = segment.upper()
            results = [r for r in results if r.segment == seg]
            
        return results

    def get_by_symbol(self, symbol: str) -> InstrumentRecord | None:
        """Return a single instrument by its normalized symbol."""
        self._ensure_loaded()
        return self._symbol_map.get(symbol.upper())

    def search(
        self, query: str, exchange: str | None = None, segment: str | None = None
    ) -> list[InstrumentRecord]:
        """Search for instruments by symbol or display name prefix/substring."""
        self._ensure_loaded()
        assert self._cache is not None
        
        q = query.upper()
        results: list[InstrumentRecord] = []
        
        for inst in self._cache:
            if exchange and inst.exchange != exchange.upper():
                continue
            if segment and inst.segment != segment.upper():
                continue
                
            if q in inst.symbol or q in inst.display_name.upper():
                results.append(inst)
                
            if len(results) >= 50:
                break
                
        return results
