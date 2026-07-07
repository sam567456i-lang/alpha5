import unittest
import yaml
import os
from Backend.Platform10.contracts.dtos import MarketStateDTO, FeatureSetDTO, ConceptSetDTO, ExecutionContext
from Backend.Platform10.engine.evaluator import MethodologyEngine

class TestTrendCoreMethodology(unittest.TestCase):
    
    def setUp(self):
        repo_root = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
        registry_path = os.path.join(repo_root, "master_capability_registry.yaml")
        with open(registry_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            
        self.registry_caps = data.get("capabilities", [])
        self.plugins_dir = os.path.join(repo_root, "Backend", "Platform10", "plugins")
        self.engine = MethodologyEngine(self.registry_caps, self.plugins_dir)
        
    def test_strong_bullish_trend(self):
        market_state = MarketStateDTO(
            symbol="BTC-USD",
            timeframe="1H",
            features=FeatureSetDTO(features={
                "TrendStructure": 0.8,
                "TrendDirection": 1.0,
                "TrendPersistence": 0.9,
                "MarketRegime": 1.0,
                "Momentum": 0.85,
                "Volatility": 0.4,
                "PricePosition": 0.7
            }),
            concepts=ConceptSetDTO(concepts={}),
            context=ExecutionContext(timestamp="2026-07-05T00:00:00Z", environment="test", run_id="run-1")
        )
        
        results, traces = self.engine.evaluate_all(market_state)
        
        trend_result = next((r for r in results if r.methodology_id == "cap_meth_trend_core"), None)
        self.assertIsNotNone(trend_result)
        
        profile = trend_result.metadata.get("TrendProfile")
        self.assertIsNotNone(profile)
        self.assertEqual(profile.direction, "Bullish")
        self.assertEqual(profile.strength, "Strong")
        self.assertEqual(profile.quality, "Good")
        self.assertEqual(trend_result.metadata.get("Methodology Health"), "Ready")
        
    def test_partial_health_missing_dependency(self):
        # Omit 'Volatility' and 'PricePosition' to trigger Partial Health gracefully
        market_state = MarketStateDTO(
            symbol="BTC-USD",
            timeframe="1H",
            features=FeatureSetDTO(features={
                "TrendStructure": 0.8,
                "TrendDirection": 1.0,
                "TrendPersistence": 0.9,
                "MarketRegime": 1.0,
                "Momentum": 0.85
            }),
            concepts=ConceptSetDTO(concepts={}),
            context=ExecutionContext(timestamp="2026-07-05T00:00:00Z", environment="test", run_id="run-2")
        )
        
        results, traces = self.engine.evaluate_all(market_state)
        trend_result = next((r for r in results if r.methodology_id == "cap_meth_trend_core"), None)
        
        self.assertEqual(trend_result.metadata.get("Methodology Health"), "Partial")
        self.assertTrue(len(trend_result.metadata.get("Confidence Provenance")) > 0)

if __name__ == '__main__':
    unittest.main()
