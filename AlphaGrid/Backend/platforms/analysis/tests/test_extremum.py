import unittest
import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.core.dto import AnalysisContext
from Backend.platforms.analysis.extremum.donchian_analysis import DonchianAnalysis
from Backend.platforms.analysis.extremum.highlow_analysis import HighLowAnalysis
from Backend.platforms.analysis.extremum.sr_analysis import SupportResistanceAnalysis

class MockIndicatorEngine:
    def __init__(self, ind_name, df):
        self.ind_name = ind_name
        self.df = df
            
    def get_indicator(self, name: str, df: pd.DataFrame, length: int = None):
        if name == self.ind_name:
            return self.df
        raise ValueError(f"Unsupported indicator: {name}")

class TestExtremumAnalysis(unittest.TestCase):
    def test_donchian_breakout_res(self):
        analysis = DonchianAnalysis()
        dc_data = pd.DataFrame({"upper": [0]*20 + [150.5], "lower": [0]*20 + [100.0]})
        engine = MockIndicatorEngine("DONCHIAN", dc_data)
        context = AnalysisContext(market_data=pd.DataFrame({"close": [150]}), timeframe="1D", dependencies={"indicator_engine": engine})
        
        res = analysis.execute(context)
        self.assertEqual(res.score, 0.70)
        self.assertEqual(res.metadata["classification"], "breakout pressure: high (resistance)")

    def test_highlow_breakout_sup(self):
        analysis = HighLowAnalysis()
        hl_data = pd.DataFrame({"highest": [0]*20 + [200.0], "lowest": [0]*20 + [149.5]})
        engine = MockIndicatorEngine("HIGHLOW", hl_data)
        context = AnalysisContext(market_data=pd.DataFrame({"close": [150]}), timeframe="1D", dependencies={"indicator_engine": engine})
        
        res = analysis.execute(context)
        self.assertEqual(res.score, -0.50)
        self.assertEqual(res.metadata["classification"], "breakout pressure: support test")

    def test_sr_critical_res(self):
        analysis = SupportResistanceAnalysis()
        sr_data = pd.DataFrame({"resistance": [150.5], "support": [100.0]})
        engine = MockIndicatorEngine("SR", sr_data)
        context = AnalysisContext(market_data=pd.DataFrame({"close": [150]}), timeframe="1D", dependencies={"indicator_engine": engine})
        
        res = analysis.execute(context)
        self.assertEqual(res.score, 0.80)
        self.assertEqual(res.metadata["classification"], "breakout pressure: critical resistance")

if __name__ == "__main__":
    unittest.main()
