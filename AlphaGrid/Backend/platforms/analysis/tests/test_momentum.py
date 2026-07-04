import unittest
import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.core.dto import AnalysisContext
from Backend.platforms.analysis.momentum.rsi_analysis import RSIAnalysis
from Backend.platforms.analysis.momentum.roc_analysis import ROCAnalysis
from Backend.platforms.analysis.momentum.macd_analysis import MACDAnalysis
from Backend.platforms.analysis.momentum.composite_momentum_analysis import CompositeMomentumAnalysis

class MockIndicatorEngine:
    def __init__(self, rsi_val=50.0, roc_val=0.0, macd_df=None):
        self.rsi_val = rsi_val
        self.roc_val = roc_val
        self.macd_df = macd_df
        
    def get_indicator(self, name: str, df: pd.DataFrame, length: int = None) -> pd.Series:
        if name == "RSI":
            return pd.Series([self.rsi_val])
        if name == "ROC":
            return pd.Series([self.roc_val])
        if name == "MACD":
            return self.macd_df
        raise ValueError(f"Unsupported indicator: {name}")

class TestMomentumAnalysis(unittest.TestCase):
    def test_rsi_overbought(self):
        analysis = RSIAnalysis()
        context = AnalysisContext(market_data=pd.DataFrame({"close": [150]}), timeframe="1D", dependencies={"indicator_engine": MockIndicatorEngine(rsi_val=85.0)})
        res = analysis.execute(context)
        print("RSI REASON:", res.metadata.get("reason"))
        self.assertEqual(res.score, -0.70)
        self.assertEqual(res.metadata["classification"], "Overbought")

    def test_roc_positive(self):
        analysis = ROCAnalysis()
        context = AnalysisContext(market_data=pd.DataFrame({"close": [150]}), timeframe="1D", dependencies={"indicator_engine": MockIndicatorEngine(roc_val=5.5)})
        res = analysis.execute(context)
        print("ROC REASON:", res.metadata.get("reason"))
        self.assertEqual(res.score, 0.60)
        self.assertEqual(res.metadata["classification"], "Positive Momentum")

    def test_macd_bullish(self):
        analysis = MACDAnalysis()
        macd_df = pd.DataFrame({
            "macd": [1.0, 1.5],
            "signal": [0.5, 0.5],
            "hist": [0.5, 1.0]
        })
        context = AnalysisContext(market_data=pd.DataFrame({"close": [150]}), timeframe="1D", dependencies={"indicator_engine": MockIndicatorEngine(macd_df=macd_df)})
        res = analysis.execute(context)
        print("MACD REASON:", res.metadata.get("reason"))
        self.assertEqual(res.score, 0.80)
        self.assertEqual(res.metadata["classification"], "Strong Bullish Momentum")

    def test_composite_momentum(self):
        from Backend.platforms.analysis.core.dto import AnalysisResult
        analysis = CompositeMomentumAnalysis()
        
        rsi_res = AnalysisResult(score=0.8, raw_data=pd.DataFrame(), signals=[], metadata={"status": "completed"})
        macd_res = AnalysisResult(score=0.7, raw_data=pd.DataFrame(), signals=[], metadata={"status": "completed"})
        
        context = AnalysisContext(market_data=pd.DataFrame({"close": [150]}), timeframe="1D", dependencies={
            "ANALYSIS_MOMENTUM_RSI": rsi_res,
            "ANALYSIS_MOMENTUM_MACD": macd_res
        })
        res = analysis.execute(context)
        print("COMPOSITE REASON:", res.metadata.get("reason"))
        
        self.assertTrue(res.score > 0)
        self.assertEqual(res.metadata["classification"], "Confirmed Bullish Momentum")

if __name__ == "__main__":
    unittest.main()
