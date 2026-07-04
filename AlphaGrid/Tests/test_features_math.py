"""Mathematical Reference Tests for Indicators."""

import unittest
import math
from typing import Dict, Any
from Shared.models.market import MarketSnapshot
from Backend.features.volatility import ATRFeature
from Backend.features.linear_regression import LinRegFeature
from Backend.features.ichimoku import TenkanSenFeature
from Backend.features.kama import KAMAFeature

import pytest
import numpy as np
import pandas as pd
from Backend.reference.legacy.features.rsi import RSIFeatureGenerator
from Backend.features.bollinger_bands import BollingerBandsFeatureGenerator
from Backend.features.stochastic_generator import StochasticFeatureGenerator
from Backend.features.keltner_channels import KeltnerChannelFeatureGenerator
from Backend.features.vwap import VWAPFeatureGenerator
class TestFeaturesMath(unittest.TestCase):
    """
    Validates features against known mathematical reference vectors.
    Ensures O(n) streaming calculation matches expected batch values.
    """

    def _make_snapshot(self, high: float, low: float, close: float) -> MarketSnapshot:
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
        for i in range(14):
            val = atr_feat.compute(self._make_snapshot(110, 100, 105), {})
            if i < 13:
                self.assertIsNone(val)
            else:
                self.assertAlmostEqual(val, 10.0, places=5)
        val2 = atr_feat.compute(self._make_snapshot(134, 110, 120), {})
        self.assertAlmostEqual(val2, 159.0 / 14.0, places=5)

    def test_linreg_math(self):
        """Verifies Linear Regression math."""
        linreg = LinRegFeature(period=5)
        # If price is strictly increasing by 1: 10, 11, 12, 13, 14
        # slope is 1, so the prediction for x=5 (end of window) should be 14 exactly.
        prices = [10, 11, 12, 13, 14]
        for i, p in enumerate(prices):
            val = linreg.compute(self._make_snapshot(p, p, p), {})
            if i < 4:
                self.assertIsNone(val)
            else:
                self.assertAlmostEqual(val, 14.0, places=5)
                
    def test_ichimoku_math(self):
        """Verifies Ichimoku Donchian logic."""
        tenkan = TenkanSenFeature() # 9 period
        prices = [10, 12, 14, 16, 18, 16, 14, 12, 10]
        # max = 18, min = 10, midpoint = 14
        for i, p in enumerate(prices):
            val = tenkan.compute(self._make_snapshot(p, p, p), {})
            if i < 8:
                self.assertIsNone(val)
            else:
                self.assertEqual(val, 14.0)

    def test_kama_math(self):
        """Verifies KAMA flat efficiency ratio handling (divide by zero protection)."""
        kama = KAMAFeature(period=4)
        prices = [10, 10, 10, 10, 10] # 5 elements (period + 1)
        for i, p in enumerate(prices):
            val = kama.compute(self._make_snapshot(p, p, p), {})
            if i < 4:
                self.assertIsNone(val)
            else:
                self.assertEqual(val, 10.0)

if __name__ == '__main__':
    unittest.main()

@pytest.fixture
def sample_data():
    np.random.seed(42)
    dates = pd.date_range(start='2026-01-01', periods=100, freq='D')
    df = pd.DataFrame({
        'open': np.random.uniform(100, 110, 100),
        'high': np.random.uniform(110, 120, 100),
        'low': np.random.uniform(90, 100, 100),
        'close': np.random.uniform(95, 115, 100),
        'volume': np.random.uniform(1000, 5000, 100)
    }, index=dates)
    df.attrs['symbol'] = 'TEST/USD'
    df.attrs['timeframe'] = '1d'
    return df

def test_rsi_determinism(sample_data):
    gen = RSIFeatureGenerator(period=14)
    dto1 = gen.generate(sample_data, "trc-1", "cor-1")
    dto2 = gen.generate(sample_data, "trc-2", "cor-2")
    
    assert dto1.values['rsi'] == dto2.values['rsi']
    assert dto1.checksum == dto2.checksum
    assert dto1.schema_version == "1.0.0"

def test_bollinger_determinism(sample_data):
    gen = BollingerBandsFeatureGenerator(period=20, std_dev=2.0)
    dto1 = gen.generate(sample_data, "trc-1", "cor-1")
    dto2 = gen.generate(sample_data, "trc-2", "cor-2")
    
    assert dto1.values['middle_band'] == dto2.values['middle_band']
    assert dto1.values['upper_band'] == dto2.values['upper_band']
    assert dto1.checksum == dto2.checksum

def test_stochastic_determinism(sample_data):
    gen = StochasticFeatureGenerator(k_period=14, d_period=3, smooth_k=3)
    dto1 = gen.generate(sample_data, "trc-1", "cor-1")
    dto2 = gen.generate(sample_data, "trc-2", "cor-2")
    
    assert dto1.values['k'] == dto2.values['k']
    assert dto1.values['d'] == dto2.values['d']
    assert dto1.checksum == dto2.checksum

def test_keltner_determinism(sample_data):
    gen = KeltnerChannelFeatureGenerator(ema_period=20, atr_period=10, atr_multiplier=2.0)
    dto1 = gen.generate(sample_data, "trc-1", "cor-1")
    dto2 = gen.generate(sample_data, "trc-2", "cor-2")
    
    assert dto1.values['middle_band'] == dto2.values['middle_band']
    assert dto1.values['upper_band'] == dto2.values['upper_band']
    assert dto1.checksum == dto2.checksum

def test_vwap_determinism(sample_data):
    gen = VWAPFeatureGenerator()
    dto1 = gen.generate(sample_data, "trc-1", "cor-1")
    dto2 = gen.generate(sample_data, "trc-2", "cor-2")
    
    assert dto1.values['vwap'] == dto2.values['vwap']
    assert dto1.checksum == dto2.checksum


def test_bollinger_bands():
    pass # Implemented in integration tests


def test_rsi():
    pass


def test_vwap():
    pass
