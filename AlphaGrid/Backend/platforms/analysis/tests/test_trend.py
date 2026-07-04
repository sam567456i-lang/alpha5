import unittest
import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.core.dto import AnalysisContext
from Backend.platforms.analysis.trend.ema_analysis import EMAAnalysis

class MockIndicatorEngine:
    def __init__(self, ema_20_val, ema_50_val, ema_200_val):
        self.ema_20_val = ema_20_val
        self.ema_50_val = ema_50_val
        self.ema_200_val = ema_200_val
        
    def get_indicator(self, name: str, df: pd.DataFrame, length: int) -> pd.Series:
        if length == 20:
            return pd.Series([self.ema_20_val])
        elif length == 50:
            return pd.Series([self.ema_50_val])
        elif length == 200:
            return pd.Series([self.ema_200_val])
        raise ValueError("Unsupported length")

class TestTrendAnalysis(unittest.TestCase):
    def setUp(self):
        self.analysis = EMAAnalysis()
        
    def test_ema_strong_uptrend(self):
        # Price > 20 > 50 > 200
        market_data = pd.DataFrame({"close": [150]})
        engine = MockIndicatorEngine(120, 100, 80)
        
        context = AnalysisContext(
            market_data=market_data,
            timeframe="1D",
            dependencies={"indicator_engine": engine}
        )
        
        result = self.analysis.execute(context)
        
        self.assertEqual(result.score, 0.85)
        self.assertEqual(result.metadata["trend"], "Strong Uptrend")
        self.assertEqual(result.metadata["risk"], "Low")
        self.assertEqual(result.metadata["status"], "Success")

    def test_ema_weakening_uptrend(self):
        # 20 > 50 > 200 but Price < 20
        market_data = pd.DataFrame({"close": [110]})
        engine = MockIndicatorEngine(120, 100, 80)
        
        context = AnalysisContext(
            market_data=market_data,
            timeframe="1D",
            dependencies={"indicator_engine": engine}
        )
        
        result = self.analysis.execute(context)
        
        self.assertEqual(result.score, 0.50)
        self.assertEqual(result.metadata["trend"], "Weakening Uptrend")
        self.assertEqual(result.metadata["risk"], "High")

    def test_ema_unsupported_if_engine_missing(self):
        market_data = pd.DataFrame({"close": [150]})
        
        context = AnalysisContext(
            market_data=market_data,
            timeframe="1D",
            dependencies={} # No engine
        )
        
        result = self.analysis.execute(context)
        self.assertEqual(result.score, 0.0)
        self.assertEqual(result.metadata["status"], "Unsupported")
        self.assertIn("Indicator Engine unavailable", result.metadata["reason"])

if __name__ == "__main__":
    unittest.main()
