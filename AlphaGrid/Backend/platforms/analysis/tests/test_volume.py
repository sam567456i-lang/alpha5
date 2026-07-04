import unittest
import pandas as pd
from typing import Dict, Any
from Backend.platforms.analysis.core.dto import AnalysisContext
from Backend.platforms.analysis.volume.vwap_analysis import VWAPAnalysis
from Backend.platforms.analysis.volume.obv_analysis import OBVAnalysis
from Backend.platforms.analysis.volume.volume_sma_analysis import VolumeSMAAnalysis
from Backend.platforms.analysis.volume.ad_analysis import AccumulationDistributionAnalysis

class MockIndicatorEngine:
    def __init__(self, ind_name, df):
        self.ind_name = ind_name
        self.df = df
            
    def get_indicator(self, name: str, df: pd.DataFrame, length: int = None):
        if name == self.ind_name:
            return self.df
        raise ValueError(f"Unsupported indicator: {name}")

class TestVolumeAnalysis(unittest.TestCase):
    def test_vwap_accumulation(self):
        analysis = VWAPAnalysis()
        vwap_data = pd.Series([100.0]*20)
        engine = MockIndicatorEngine("VWAP", vwap_data)
        context = AnalysisContext(market_data=pd.DataFrame({"close": [101.0]*20}), timeframe="1D", dependencies={"indicator_engine": engine})
        
        res = analysis.execute(context)
        self.assertEqual(res.score, 0.60)
        self.assertEqual(res.metadata["classification"], "accumulation")

    def test_obv_weakness(self):
        analysis = OBVAnalysis()
        obv_data = pd.Series([1000, 900, 800, 700, 600] + [500]*15)
        engine = MockIndicatorEngine("OBV", obv_data)
        context = AnalysisContext(market_data=pd.DataFrame({"close": [150]*20}), timeframe="1D", dependencies={"indicator_engine": engine})
        
        res = analysis.execute(context)
        self.assertEqual(res.score, -0.50)
        self.assertEqual(res.metadata["classification"], "volume weakness")

    def test_vsma_confirmation(self):
        analysis = VolumeSMAAnalysis()
        vsma_data = pd.Series([1000]*20)
        engine = MockIndicatorEngine("VOLUME_SMA", vsma_data)
        context = AnalysisContext(market_data=pd.DataFrame({"close": [150]*20, "volume": [1600]*20}), timeframe="1D", dependencies={"indicator_engine": engine})
        
        res = analysis.execute(context)
        self.assertEqual(res.score, 0.60)
        self.assertEqual(res.metadata["classification"], "volume confirmation")

    def test_ad_accumulation(self):
        analysis = AccumulationDistributionAnalysis()
        ad_data = pd.Series([1000, 1100])
        engine = MockIndicatorEngine("ACC_DIST", ad_data)
        context = AnalysisContext(market_data=pd.DataFrame({"close": [150]*2}), timeframe="1D", dependencies={"indicator_engine": engine})
        
        res = analysis.execute(context)
        self.assertEqual(res.score, 0.55)
        self.assertEqual(res.metadata["classification"], "accumulation")

if __name__ == "__main__":
    unittest.main()
