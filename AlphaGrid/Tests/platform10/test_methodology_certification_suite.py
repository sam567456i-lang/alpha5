import unittest
import os
from Backend.platforms.platform10_methodologies.runtime.methodology_runtime import MethodologyRuntime
from Backend.core.interfaces.methodology_context_dto import MethodologyContextDTO
from Backend.core.interfaces.execution_mode_dto import ExecutionModeDTO, ExecutionMode

class TestMethodologyCertificationSuite(unittest.TestCase):
    def setUp(self):
        self.registry_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Docs", "Governance", "registry"))
        self.runtime = MethodologyRuntime(self.registry_dir)
        self.context = MethodologyContextDTO(
            identity="test_context_001",
            market_identity="NQ",
            symbol="NQ=F",
            timeframe="5m",
            session="RTH",
            execution_mode=ExecutionModeDTO(mode=ExecutionMode.REPLAY, description="Testing replay mode")
        )

    def test_determinism_and_consensus(self):
        result = self.runtime.evaluate_context(self.context)
        
        # Verify consensus generation
        consensus = result.get("consensus")
        self.assertIsNotNone(consensus)
        self.assertEqual(consensus.active_methodology_count, 2)
        
        # Verify mock conflict (ICT Bullish vs Wyckoff Distribution)
        self.assertTrue("Bullish" in consensus.probabilities)
        self.assertTrue("Distribution" in consensus.probabilities)
        
        # Verify deterministic output (should be exactly 50/50 given 2 mock plugins)
        self.assertEqual(consensus.probabilities["Bullish"], 0.5)
        self.assertEqual(consensus.probabilities["Distribution"], 0.5)

if __name__ == '__main__':
    unittest.main()
