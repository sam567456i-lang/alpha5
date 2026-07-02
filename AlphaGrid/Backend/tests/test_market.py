"""Unit tests for the Market Intelligence platform core engines."""

from __future__ import annotations

import unittest
from datetime import datetime, timezone
from decimal import Decimal

from Shared.models.market import MarketSnapshot

from Backend.market.breadth import MarketBreadthCalculator
from Backend.market.connector_manager import ConnectorManager
from Backend.market.instruments import InstrumentCatalog
from Backend.market.live_quotes import LiveQuoteEngine
from Backend.market.normalizer import DataNormalizer
from Backend.market.ohlcv import OHLCVEngine
from Backend.market.providers.base import (
    LiveQuoteRecord,
    OHLCVRecord,
    ValidationStatus,
)
from Backend.market.providers.mock import MockProvider
from Backend.market.regime import RegimeDetector
from Backend.market.session import MarketSessionManager
from Backend.market.validator import OHLCVValidator


class OHLCVValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base_record = OHLCVRecord(
            symbol="TEST",
            exchange="NSE",
            timeframe="1d",
            timestamp=datetime.now(timezone.utc),
            open=Decimal("100"),
            high=Decimal("110"),
            low=Decimal("90"),
            close=Decimal("105"),
            volume=1000,
        )

    def test_valid_record_passes(self) -> None:
        result = OHLCVValidator.validate(self.base_record)
        self.assertEqual(result.status, ValidationStatus.PASS)

    def test_high_lower_than_open_fails(self) -> None:
        from dataclasses import replace

        bad = replace(self.base_record, high=Decimal("95"))
        result = OHLCVValidator.validate(bad)
        self.assertEqual(result.status, ValidationStatus.FAIL)

    def test_low_higher_than_close_fails(self) -> None:
        from dataclasses import replace

        bad = replace(self.base_record, low=Decimal("108"))
        result = OHLCVValidator.validate(bad)
        self.assertEqual(result.status, ValidationStatus.FAIL)

    def test_negative_volume_fails(self) -> None:
        from dataclasses import replace

        bad = replace(self.base_record, volume=-100)
        result = OHLCVValidator.validate(bad)
        self.assertEqual(result.status, ValidationStatus.FAIL)


class DataNormalizerTests(unittest.TestCase):
    def test_normalize_symbol(self) -> None:
        self.assertEqual(DataNormalizer._normalize_symbol("RELIANCE.NS"), "RELIANCE")
        self.assertEqual(DataNormalizer._normalize_symbol("TCS.BO"), "TCS")
        self.assertEqual(DataNormalizer._normalize_symbol("NIFTY"), "NIFTY")

    def test_normalize_exchange(self) -> None:
        self.assertEqual(DataNormalizer._normalize_exchange("nse_eq"), "NSE")
        self.assertEqual(DataNormalizer._normalize_exchange("BSE_FO"), "BSE")

    def test_normalize_ohlcv_coerces_utc(self) -> None:
        # Naive datetime
        naive = datetime(2026, 6, 30, 10, 0)
        rec = OHLCVRecord(
            symbol="TCS",
            exchange="NSE",
            timeframe="15m",
            timestamp=naive,
            open=Decimal(10),
            high=Decimal(10),
            low=Decimal(10),
            close=Decimal(10),
            volume=100,
        )
        snap = DataNormalizer.normalize_ohlcv(rec)
        self.assertEqual(snap.timestamp.tzinfo, timezone.utc)


class MarketBreadthCalculatorTests(unittest.TestCase):
    def test_calculate_breadth(self) -> None:
        def make_quote(op: float, cl: float) -> MarketSnapshot:
            return MarketSnapshot(
                symbol="SYM",
                exchange="NSE",
                instrument_type="STOCK",
                timestamp=datetime.now(timezone.utc),
                last_price=Decimal(cl),
                open=Decimal(op),
                high=Decimal(max(op, cl)),
                low=Decimal(min(op, cl)),
                close=Decimal(cl),
                volume=100,
            )

        quotes = [
            make_quote(100, 105),  # Advance
            make_quote(100, 110),  # Advance
            make_quote(100, 95),   # Decline
            make_quote(100, 100),  # Unchanged
        ]

        metrics = MarketBreadthCalculator.calculate_breadth(quotes)
        self.assertEqual(metrics["advances"], 2)
        self.assertEqual(metrics["declines"], 1)
        self.assertEqual(metrics["unchanged"], 1)
        self.assertEqual(metrics["ad_ratio"], 2.0)
        # 2 advances / (2 advances + 1 decline) = 0.6667
        self.assertEqual(metrics["breadth_score"], 0.6667)


class RegimeDetectorTests(unittest.TestCase):
    def test_bullish_trending(self) -> None:
        r = RegimeDetector.detect_regime(breadth_score=0.75, vix_value=14.0, trend_strength=0.7)
        self.assertEqual(r["regime"], "TRENDING_BULLISH")

    def test_high_volatility(self) -> None:
        r = RegimeDetector.detect_regime(breadth_score=0.5, vix_value=28.0, trend_strength=0.3)
        self.assertEqual(r["regime"], "HIGH_VOLATILITY")


class ConnectorManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = ConnectorManager()
        self.manager.register(MockProvider())

    def test_get_instruments_success(self) -> None:
        insts = self.manager.get_instruments()
        self.assertGreater(len(insts), 0)

    def test_failover_when_primary_fails(self) -> None:
        # We simulate this by relying on the fact that if a provider fails,
        # it drops to the next one. MockProvider never fails.
        class BadProvider(MockProvider):
            @property
            def provider_name(self) -> str:
                return "bad"

            def get_live_quote(self, symbol: str, exchange: str) -> LiveQuoteRecord:
                from Backend.market.providers.base import ProviderUnavailable
                raise ProviderUnavailable(self.provider_name, "Simulated failure")

        self.manager.register(BadProvider())
        # Set bad provider as primary
        self.manager.set_priority(["bad", "mock"])
        
        # Should succeed by falling through to mock
        quote = self.manager.get_live_quote("NIFTY", "NSE")
        self.assertIsNotNone(quote)


class OHLCVEngineTests(unittest.TestCase):
    def test_fetch_and_normalize(self) -> None:
        mgr = ConnectorManager()
        mgr.register(MockProvider())
        catalog = InstrumentCatalog(mgr)
        engine = OHLCVEngine(mgr, catalog)

        from_dt = datetime(2026, 6, 1, tzinfo=timezone.utc)
        to_dt = datetime(2026, 6, 2, tzinfo=timezone.utc)
        
        snaps = engine.get_ohlcv("NIFTY", "1h", from_dt, to_dt)
        self.assertGreater(len(snaps), 0)
        self.assertIsInstance(snaps[0], MarketSnapshot)


class SessionManagerTests(unittest.TestCase):
    def test_is_holiday(self) -> None:
        mgr = MarketSessionManager()
        # Jan 26 is a holiday
        self.assertTrue(mgr.is_holiday(datetime(2026, 1, 26).date()))


class ConcurrencyTests(unittest.TestCase):
    def test_concurrent_provider_registration(self) -> None:
        manager = ConnectorManager()
        
        def worker(i: int) -> None:
            class DummyProvider(MockProvider):
                @property
                def provider_name(self) -> str:
                    return f"dummy_{i}"
            manager.register(DummyProvider())

        import threading
        for _ in range(50):
            threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            
        self.assertEqual(len(manager._providers), 10)

    def test_concurrent_cache_access(self) -> None:
        manager = ConnectorManager()
        manager.register(MockProvider())
        catalog = InstrumentCatalog(manager)
        engine = LiveQuoteEngine(manager, catalog)
        
        import threading
        
        def worker() -> None:
            engine.get_live_quote("NIFTY")
            
        for _ in range(50):
            threads = [threading.Thread(target=worker) for _ in range(10)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
                
        self.assertIn("NIFTY", engine._cache)

    def test_concurrent_catalog_lazy_init(self) -> None:
        import threading
        for _ in range(50):
            manager = ConnectorManager()
            manager.register(MockProvider())
            catalog = InstrumentCatalog(manager)
            
            def worker() -> None:
                catalog.get_by_symbol("NIFTY")
                
            threads = [threading.Thread(target=worker) for _ in range(10)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
                
            self.assertIsNotNone(catalog._cache)
