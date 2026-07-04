import unittest
import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.core.dto import AnalysisContext
from Backend.platforms.analysis.momentum.rsi_analysis import RSIAnalysis

class MockIndicatorEngine:
    def __init__(self, rsi_val=50.0, roc_val=0.0):
        self.rsi_val = rsi_val
        self.roc_val = roc_val
        
    def get_indicator(self, name: str, df: pd.DataFrame, length: int) -> pd.Series:
        if name == "RSI" and length == 14:
            return pd.Series([self.rsi_val])
        if name == "ROC" and length == 9:
            return pd.Series([self.roc_val])
        raise ValueError("Unsupported length/indicator")

class TestMomentumAnalysis(unittest.TestCase):
    def setUp(self):
        self.analysis = RSIAnalysis()
        
    def test_rsi_overbought(self):
        market_data = pd.DataFrame({"close": [150]})
        engine = MockIndicatorEngine(85.0)
        
        context = AnalysisContext(
            market_data=market_data,
            timeframe="1D",
            dependencies={"indicator_engine": engine}
        )
        
        result = self.analysis.execute(context)
        
        self.assertEqual(result.score, -0.70)
        self.assertEqual(result.metadata["classification"], "Overbought")
        self.assertEqual(result.metadata["risk_flags"], ["High (Reversal Risk)"])

    def test_rsi_oversold(self):
        market_data = pd.DataFrame({"close": [110]})
        engine = MockIndicatorEngine(20.0)
        
        context = AnalysisContext(
            market_data=market_data,
            timeframe="1D",
            dependencies={"indicator_engine": engine}
        )
        
        result = self.analysis.execute(context)
        
        self.assertEqual(result.score, 0.70)
        self.assertEqual(result.metadata["classification"], "Oversold")

from Backend.platforms.analysis.momentum.roc_analysis import ROCAnalysis

class TestROCAnalysis(unittest.TestCase):
    def setUp(self):
        self.analysis = ROCAnalysis()
        
    def test_roc_positive(self):
        market_data = pd.DataFrame({"close": [150]})
        engine = MockIndicatorEngine(roc_val=5.5)
        context = AnalysisContext(market_data=market_data, timeframe="1D", dependencies={"indicator_engine": engine})
        result = self.analysis.execute(context)
        
        self.assertEqual(result.score, 0.60)
        self.assertEqual(result.metadata["classification"], "Positive Momentum")

    def test_roc_negative(self):
        market_data = pd.DataFrame({"close": [150]})
        engine = MockIndicatorEngine(roc_val=-2.5)
        context = AnalysisContext(market_data=market_data, timeframe="1D", dependencies={"indicator_engine": engine})
        result = self.analysis.execute(context)
        
        self.assertEqual(result.score, -0.60)
        self.assertEqual(result.metadata["classification"], "Negative Momentum")

if __name__ == "__main__":
    unittest.main()
