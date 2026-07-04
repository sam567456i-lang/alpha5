import unittest
import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.core.dto import AnalysisContext
from Backend.platforms.analysis.volatility.atr_analysis import ATRAnalysis

class MockIndicatorEngine:
    def __init__(self, atr_val=1.0, atr_series=None):
        if atr_series is not None:
            self.atr_series = atr_series
        else:
            # mock 20 days of ATR
            self.atr_series = pd.Series([atr_val]*20)
            
    def get_indicator(self, name: str, df: pd.DataFrame, length: int = None) -> pd.Series:
        if name == "ATR":
            return self.atr_series
        raise ValueError(f"Unsupported indicator: {name}")

class TestVolatilityAnalysis(unittest.TestCase):
    def test_atr_expansion(self):
        analysis = ATRAnalysis()
        # Create a series where current ATR is much higher than previous
        atr_data = [1.0] * 19 + [2.0]
        engine = MockIndicatorEngine(atr_series=pd.Series(atr_data))
        context = AnalysisContext(market_data=pd.DataFrame({"close": [150]}), timeframe="1D", dependencies={"indicator_engine": engine})
        
        res = analysis.execute(context)
        self.assertEqual(res.score, 0.50)
        self.assertEqual(res.metadata["classification"], "expansion")

    def test_atr_contraction(self):
        analysis = ATRAnalysis()
        # Create a series where current ATR is much lower than previous
        atr_data = [2.0] * 19 + [1.0]
        engine = MockIndicatorEngine(atr_series=pd.Series(atr_data))
        context = AnalysisContext(market_data=pd.DataFrame({"close": [150]}), timeframe="1D", dependencies={"indicator_engine": engine})
        
        res = analysis.execute(context)
        self.assertEqual(res.score, -0.50)
        self.assertEqual(res.metadata["classification"], "contraction")

from Backend.platforms.analysis.volatility.bollinger_analysis import BollingerAnalysis
from Backend.platforms.analysis.volatility.keltner_analysis import KeltnerAnalysis

class TestBollingerAnalysis(unittest.TestCase):
    def test_bb_expansion(self):
        analysis = BollingerAnalysis()
        bb_data = pd.DataFrame({
            "upper": [0]*20, "middle": [0]*20, "lower": [0]*20,
            "bandwidth": [1.0]*19 + [1.5]
        })
        engine = MockIndicatorEngine(atr_val=1.0)
        engine.get_indicator = lambda name, df, length=None: bb_data if name == "BOLLINGER_BANDS" else pd.Series()
        context = AnalysisContext(market_data=pd.DataFrame({"close": [150]}), timeframe="1D", dependencies={"indicator_engine": engine})
        
        res = analysis.execute(context)
        self.assertEqual(res.score, 0.60)
        self.assertEqual(res.metadata["classification"], "expansion")

class TestKeltnerAnalysis(unittest.TestCase):
    def test_kc_compression(self):
        analysis = KeltnerAnalysis()
        kc_data = pd.DataFrame({
            "upper": [0]*20, "middle": [0]*20, "lower": [0]*20,
            "bandwidth": [1.0]*19 + [0.90]
        })
        engine = MockIndicatorEngine(atr_val=1.0)
        engine.get_indicator = lambda name, df, length=None: kc_data if name == "KELTNER_CHANNELS" else pd.Series()
        context = AnalysisContext(market_data=pd.DataFrame({"close": [150]}), timeframe="1D", dependencies={"indicator_engine": engine})
        
        res = analysis.execute(context)
        self.assertEqual(res.score, -0.40)
        self.assertEqual(res.metadata["classification"], "compression")

if __name__ == "__main__":
    unittest.main()
