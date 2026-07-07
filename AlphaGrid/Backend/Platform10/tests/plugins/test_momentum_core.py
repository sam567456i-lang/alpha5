import unittest
from Backend.Platform10.plugins.momentum_core import MomentumCoreMethodology
from Backend.Platform10.contracts.dtos import MarketStateDTO, FeatureSetDTO, ConceptSetDTO, ExecutionContext

class TestMomentumCoreMethodology(unittest.TestCase):
    def setUp(self):
        self.plugin = MomentumCoreMethodology()
        self.context = ExecutionContext(timestamp="2026-07-05T00:00:00Z", environment="TEST", run_id="run_1")

    def test_bullish_momentum_ready(self):
        # All required capabilities present
        features = {
            "MomentumDirection": 1.0,
            "MomentumVelocity": 0.85, # Extreme
            "MomentumAcceleration": 0.2, # Increasing
            "MomentumPersistence": 0.8, # High
            "MomentumDivergence": 0.0, # None
            "TrendState": 1.0,
            "MarketRegime": 1.0 # Trending
        }
        
        state = MarketStateDTO(
            symbol="BTC/USD", timeframe="1H",
            features=FeatureSetDTO(features=features),
            concepts=ConceptSetDTO(concepts={}),
            context=self.context
        )
        
        factors, metadata = self.plugin.evaluate_factors(state)
        
        self.assertEqual(metadata["Methodology Health"], "Ready")
        self.assertEqual(metadata["Applicability Score"], 1.0)
        self.assertEqual(metadata["Reliability Score"], 1.0)
        self.assertEqual(metadata["MomentumProfile"].direction, "Bullish")
        self.assertEqual(metadata["MomentumProfile"].velocity, "Extreme")
        self.assertEqual(metadata["MomentumProfile"].acceleration, "Increasing")
        self.assertEqual(metadata["MomentumProfile"].exhaustion, "High") # 0.85 - 0.2 = 0.65 -> High
        self.assertEqual(metadata["MomentumProfile"].divergence, "None")
        
    def test_momentum_exhaustion_with_divergence(self):
        features = {
            "MomentumDirection": 1.0,
            "MomentumVelocity": 0.9, # Extreme
            "MomentumAcceleration": -0.15, # Decreasing
            "MomentumPersistence": 0.8, 
            "MomentumDivergence": -1.0, # Bearish Regular Divergence
            "TrendState": 1.0,
            "MarketRegime": 1.0 
        }
        
        state = MarketStateDTO(
            symbol="BTC/USD", timeframe="1H",
            features=FeatureSetDTO(features=features),
            concepts=ConceptSetDTO(concepts={}),
            context=self.context
        )
        
        factors, metadata = self.plugin.evaluate_factors(state)
        
        self.assertEqual(metadata["Methodology Health"], "Ready")
        # 0.9 - (-0.15) = 1.05 and Divergence != None -> Critical Exhaustion
        self.assertEqual(metadata["MomentumProfile"].exhaustion, "Critical")
        self.assertEqual(metadata["MomentumProfile"].divergence, "Bearish Regular")
        self.assertEqual(metadata["Reliability Score"], 0.3) # Conflicting concepts reduce reliability
        self.assertIn("Bearish Divergence (Warning)", metadata["conflicting_concepts"])
        self.assertIn("Momentum Exhaustion", metadata["conflicting_concepts"])
        
    def test_partial_health(self):
        # Missing divergence and persistence
        features = {
            "MomentumDirection": -1.0,
            "MomentumVelocity": 0.3, # Moderate
            "MomentumAcceleration": 0.0, # Stable
            "TrendState": -1.0,
            "MarketRegime": 0.0 # Ranging
        }
        
        state = MarketStateDTO(
            symbol="BTC/USD", timeframe="1H",
            features=FeatureSetDTO(features=features),
            concepts=ConceptSetDTO(concepts={}),
            context=self.context
        )
        
        factors, metadata = self.plugin.evaluate_factors(state)
        
        self.assertEqual(metadata["Methodology Health"], "Partial")
        # 2 missing -> 1.0 - 0.3 = 0.7 applicability
        self.assertAlmostEqual(metadata["Applicability Score"], 0.7)
        self.assertEqual(metadata["MomentumProfile"].direction, "Bearish")
        self.assertEqual(metadata["MomentumProfile"].velocity, "Moderate")
        self.assertEqual(metadata["MomentumProfile"].acceleration, "Stable")
        self.assertEqual(metadata["MomentumProfile"].regime_compatibility, "Ranging")

if __name__ == "__main__":
    unittest.main()
