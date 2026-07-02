"""Mathematical Reference Tests for Indicators."""

import unittest
import math
from typing import Dict, Any
from Shared.models.market import MarketSnapshot
from Backend.features.volatility import ATRFeature

class TestFeaturesMath(unittest.TestCase):
    """
    Validates features against known mathematical reference vectors.
    Ensures O(n) streaming calculation matches expected batch values.
    """

    def _make_snapshot(self, high: float, low: float, close: float) -> MarketSnapshot:
        # We can construct a dict and the tests could pass it if engine was doing normalization,
        # but here we test the feature directly so we pass MarketSnapshot.
        from datetime import datetime, timezone
        return MarketSnapshot(
            symbol="BTCUSD",
            exchange="BINANCE",
            instrument_type="SPOT",
            last_price=close,
            open=low, # Dummy
            high=high,
            low=low,
            close=close,
            volume=1000,
            timestamp=datetime(2025, 1, 1, tzinfo=timezone.utc)
        )

    def test_atr_math(self):
        """Verifies Wilder's Smoothing for ATR."""
        atr_feat = ATRFeature(period=14)
        
        # We use a synthetic linear TR sequence where TR is exactly 10 every bar.
        # High = 110, Low = 100, Close = 105. TR = max(110-100, 110-prev, prev-100) = 10.
        for i in range(14):
            val = atr_feat.compute(self._make_snapshot(110, 100, 105), {})
            if i < 13:
                self.assertIsNone(val)
            else:
                self.assertAlmostEqual(val, 10.0, places=5)
                
        # Now introduce a jump where TR = 29. High=134, Low=110, prevClose=105. 
        val2 = atr_feat.compute(self._make_snapshot(134, 110, 120), {})
        # Wilder's Smoothing: (PrevATR * 13 + TR) / 14 = (10 * 13 + 29) / 14 = 159 / 14 = 11.35714...
        self.assertAlmostEqual(val2, 159.0 / 14.0, places=5)

if __name__ == '__main__':
    unittest.main()
