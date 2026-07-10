import unittest
from datetime import datetime
from Backend.core.methodologies.core_models import MethodologyContext, MethodologyDefinition, MethodologyVersion, MethodologyInstance
from Backend.core.methodologies.registry import MethodologyRegistry, MethodologyManifest, CapabilityNegotiation, Namespace, MethodologyLifecycle
from Backend.core.methodologies.evidence import MethodologyClaim

class MockValidMethodology(MethodologyInstance):
    def evaluate(self, context: MethodologyContext):
        # Simply returns a mock state without mutating context
        return []

class MockMutatingMethodology(MethodologyInstance):
    def evaluate(self, context: MethodologyContext):
        # Illegally attempt to mutate frozen context
        context.symbol = "ETH"
        return []

class TestMethodologyConformance(unittest.TestCase):
    def setUp(self):
        self.context = MethodologyContext(
            context_id="ctx_001",
            symbol="BTCUSDT",
            timeframe="1H",
            execution_timestamp=datetime.now(),
            market_regime="TREND",
            available_capabilities=["Liquidity", "Structure"],
            object_graph_snapshot={},
            feature_snapshot={},
            data_quality_score=0.99,
            degradation_state="NONE"
        )
        self.definition = MethodologyDefinition("mock_1", "Mock", "Mock Def")
        self.version = MethodologyVersion(self.definition, "v1.0", "r1")

    def test_context_immutability(self):
        """Verifies that a methodology cannot mutate the context snapshot."""
        instance = MockMutatingMethodology("inst_1", self.version, "BTCUSDT", "1H")
        
        with self.assertRaises(Exception): # frozen dataclass throws FrozenInstanceError
            instance.evaluate(self.context)
            
    def test_capability_negotiation(self):
        """Verifies that the CapabilityNegotiation degrades unsupported methodologies."""
        manifest = MethodologyManifest(
            version_ref=self.version,
            namespace=Namespace.BUILT_IN,
            lifecycle=MethodologyLifecycle.PRODUCTION,
            requires_families=["Liquidity", "OrderFlow"] # OrderFlow is missing in context
        )
        status = CapabilityNegotiation.negotiate(manifest, self.context)
        self.assertEqual(status, "UNSUPPORTED")

if __name__ == '__main__':
    unittest.main()
