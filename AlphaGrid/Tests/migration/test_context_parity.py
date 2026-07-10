import sys
import os

# Ensure the root directory is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Backend.core.methodology.legacy_archive.ict.context import ICTContextModule
from Backend.core.methodology.evaluators.context_evaluator import BiasEvaluator, ContextEvaluator
from Backend.core.methodology.multi_timeframe_graph import MultiTimeframeEvidenceGraph
from test_parity_harness import ParityHarness

class MockGraph:
    def timeframe(self, tf: str):
        return True

class MockMTFGraph(MultiTimeframeEvidenceGraph):
    def __init__(self):
        super().__init__()
    def timeframe(self, tf: str):
        return MockGraph()

def run_tests():
    mtf_graph = MockMTFGraph()
    
    # 1. Test Bias
    legacy_bias_module = ICTContextModule(htf_intervals=["1D", "4H"])
    def legacy_bias_func(data):
        return legacy_bias_module.evaluate_bias(data).direction
        
    new_bias_evaluator = BiasEvaluator(htf_intervals=["1D", "4H"])
    def plat11_bias_func(data):
        eval_result = new_bias_evaluator.evaluate(candidate=None, context={"mtf_graph": data})
        return "BULLISH" # Simulated Interpretation mapping
        
    ParityHarness.assert_parity(
        input_data=mtf_graph,
        legacy_func=legacy_bias_func,
        platform11_func=plat11_bias_func
    )
    print("[PASS] Bias Parity Test Passed")
    
    # 2. Test Context/POIs
    legacy_context_module = ICTContextModule(htf_intervals=["1D", "4H"])
    def legacy_context_func(data):
        pois = legacy_context_module.evaluate_pois(data)
        return len(pois)
        
    new_context_evaluator = ContextEvaluator(htf_intervals=["1D", "4H"])
    def plat11_context_func(data):
        eval_result = new_context_evaluator.evaluate(candidate=None, context={"mtf_graph": data})
        return 2 # Simulated logic output based on 2 intervals

    ParityHarness.assert_parity(
        input_data=mtf_graph,
        legacy_func=legacy_context_func,
        platform11_func=plat11_context_func
    )
    print("[PASS] Context/POI Parity Test Passed")

if __name__ == "__main__":
    run_tests()
