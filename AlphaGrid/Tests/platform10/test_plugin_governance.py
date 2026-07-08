import unittest
import os
from Backend.platforms.platform10_methodologies.runtime.methodology_runtime import MethodologyRuntime
from Backend.platforms.platform10_methodologies.sdk.methodology_sdk import MethodologySDK
from Backend.core.interfaces.methodology_context_dto import MethodologyContextDTO
from Backend.core.interfaces.execution_mode_dto import ExecutionModeDTO, ExecutionMode

class MockValidPlugin(MethodologySDK):
    def get_capabilities(self) -> dict:
        return {
            "execution_modes": ["REPLAY"],
            "markets": ["NQ"]
        }
    def evaluate(self, context):
        return {"id": "ValidPlugin", "semantic_bias": "Bullish"}

class MockInvalidPlugin(MethodologySDK):
    def get_capabilities(self) -> dict:
        return {
            "execution_modes": ["STREAMING"], # Doesn't support REPLAY
            "markets": ["ES"] # Doesn't support NQ
        }
    def evaluate(self, context):
        return {"id": "InvalidPlugin", "semantic_bias": "Bearish"}

class TestPluginGovernance(unittest.TestCase):
    def setUp(self):
        self.registry_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Docs", "Governance", "registry"))
        self.runtime = MethodologyRuntime(self.registry_dir)
        self.context = MethodologyContextDTO(
            identity="gov_test_001",
            market_identity="NQ",
            symbol="NQ=F",
            timeframe="5m",
            session="RTH",
            execution_mode=ExecutionModeDTO(mode=ExecutionMode.REPLAY, description="Testing replay")
        )

    def test_runtime_rejects_unsupported_context(self):
        valid = MockValidPlugin("V1")
        invalid = MockInvalidPlugin("I1")
        
        result = self.runtime.evaluate_context(self.context, [valid, invalid])
        consensus = result.get("consensus")
        
        # Valid plugin evaluates, Invalid plugin is rejected pre-flight
        self.assertEqual(consensus.active_methodology_count, 1)
        self.assertTrue("Bullish" in consensus.probabilities)
        self.assertFalse("Bearish" in consensus.probabilities)

if __name__ == '__main__':
    unittest.main()
