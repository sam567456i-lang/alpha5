import pytest
from datetime import datetime
from Backend.market_intelligence.market_state_engine import MarketStateEngine, MarketState
from Backend.foundation.exceptions import DataError

class CorruptCalendar:
    def is_holiday(self, timestamp, exchange):
        raise ValueError("Corrupt Calendar Data: Invalid Holiday Matrix")

class MissingExchangeCalendar:
    def is_holiday(self, timestamp, exchange):
        if exchange == "UNKNOWN":
            raise KeyError("Exchange UNKNOWN not found in registry")
        return False

class TestFaultInjection:
    def test_corrupt_calendar_graceful_failure(self):
        engine = MarketStateEngine(trading_calendar=CorruptCalendar())
        # Should the system crash or fail gracefully? 
        # The engine currently just crashes if the calendar raises ValueError.
        # Let's catch it and fallback to CLOSED in the engine, or expect it to bubble up to be caught by the orchestrator.
        # Actually, institutional rules prefer fast failures over silent closed states if the calendar is truly corrupt.
        with pytest.raises(ValueError, match="Corrupt Calendar Data"):
            engine.get_current_state(datetime.now(), "NSE")

    def test_missing_exchange(self):
        engine = MarketStateEngine(trading_calendar=MissingExchangeCalendar())
        with pytest.raises(KeyError, match="Exchange UNKNOWN not found"):
            engine.get_current_state(datetime.now(), "UNKNOWN")

    def test_invalid_metadata(self):
        # We don't have a formal SymbolMetadata class yet (planned for Phase 10B registry verification),
        # but fault injection tests the assumption that if an engine receives invalid data, it rejects it.
        pass
