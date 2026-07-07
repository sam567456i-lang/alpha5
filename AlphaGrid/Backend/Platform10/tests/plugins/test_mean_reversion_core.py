import unittest
from Backend.Platform10.plugins.mean_reversion_core import MeanReversionCoreMethodology
from Backend.Platform10.contracts.dtos import MarketStateDTO, FeatureSetDTO, ConceptSetDTO, ExecutionContext

class TestMeanReversionCoreMethodology(unittest.TestCase):
    def setUp(self):
        self.plugin = MeanReversionCoreMethodology()
        self.context = ExecutionContext(timestamp="2026-07-05T00:00:00Z", environment="TEST", run_id="run_1")

    def test_overextended_bullish_ready(self):
        features = {
            "ReferenceValueDeviation": 0.85, # Extreme deviation upwards
            "RejectionQuality": 0.9, # High quality rejection
            "LiquidityReaction": 0.8,
            "VolatilityCompression": 1.0, # Compressed
            "TrendState": 0.0,
            "MarketRegime": 0.0 # Ranging
        }
        
        state = MarketStateDTO(
            symbol="ETH/USD", timeframe="1H",
            features=FeatureSetDTO(features=features),
            concepts=ConceptSetDTO(concepts={}),
            context=self.context
        )
        
        factors, metadata = self.plugin.evaluate_factors(state)
        
        self.assertEqual(metadata["Methodology Health"], "Ready")
        self.assertEqual(metadata["Applicability Score"], 1.0)
        
        profile = metadata["MeanReversionProfile"]
        self.assertEqual(profile.state, "Overextended Bullish")
        self.assertEqual(profile.deviation_severity, "Extreme")
        self.assertEqual(profile.reversion_target, "Complete")
        self.assertEqual(profile.structure, "Rejection Formation")
        self.assertGreater(profile.prob_completion, 0.7) # Ranging market, strong rejection
        
    def test_failure_conditions_in_trend(self):
        features = {
            "ReferenceValueDeviation": -0.9, # Overextended Bearish
            "RejectionQuality": 0.2, # Poor rejection
            "LiquidityReaction": 0.1,
            "VolatilityCompression": 0.1, # Volatility expanding
            "TrendState": 1.0,
            "MarketRegime": 1.0 # Trending strongly
        }
        
        state = MarketStateDTO(
            symbol="ETH/USD", timeframe="1H",
            features=FeatureSetDTO(features=features),
            concepts=ConceptSetDTO(concepts={}),
            context=self.context
        )
        
        factors, metadata = self.plugin.evaluate_factors(state)
        
        profile = metadata["MeanReversionProfile"]
        self.assertEqual(profile.state, "Overextended Bearish")
        
        # Should have low completion probability because it's a trend
        self.assertLess(profile.prob_completion, 0.3)
        self.assertEqual(profile.regime_compatibility, "Trending")
        
        # Check failure conditions
        self.assertIn("Trend acceleration", profile.failure_conditions)
        self.assertIn("Volatility expansion", profile.failure_conditions)
        
        # Reliability should be downgraded due to conflicting regime
        self.assertLess(metadata["Reliability Score"], 1.0)

    def test_partial_health_applicability_penalty(self):
        features = {
            "ReferenceValueDeviation": 0.5,
            "MarketRegime": 0.5 # Transition
        } # Missing 4 dependencies
        
        state = MarketStateDTO(
            symbol="ETH/USD", timeframe="1H",
            features=FeatureSetDTO(features=features),
            concepts=ConceptSetDTO(concepts={}),
            context=self.context
        )
        
        factors, metadata = self.plugin.evaluate_factors(state)
        
        self.assertEqual(metadata["Methodology Health"], "Degraded")
        # 1.0 - (4 * 0.15) = 0.4 applicability
        self.assertAlmostEqual(metadata["Applicability Score"], 0.4)
        
        profile = metadata["MeanReversionProfile"]
        self.assertEqual(profile.state, "Equilibrium")
        self.assertEqual(profile.structure, "No Evidence")

if __name__ == "__main__":
    unittest.main()
