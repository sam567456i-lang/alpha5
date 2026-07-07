import unittest
import yaml
import os
from Backend.Platform10.contracts.dtos import MarketStateDTO, FeatureSetDTO, ConceptSetDTO, ExecutionContext, MethodologyResultDTO
from Backend.Platform10.engine.loader import PluginLoader
from Backend.Platform10.engine.evaluator import MethodologyEngine

class TestPlatform10Engine(unittest.TestCase):
    
    def setUp(self):
        repo_root = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid"
        registry_path = os.path.join(repo_root, "master_capability_registry.yaml")
        with open(registry_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            
        self.registry_caps = data.get("capabilities", [])
        self.plugins_dir = os.path.join(repo_root, "Backend", "Platform10", "plugins")
        self.engine = MethodologyEngine(self.registry_caps, self.plugins_dir)
        
    def test_plugin_discovery_and_versioning(self):
        plugins = self.engine.loader.get_all_plugins()
        self.assertTrue(len(plugins) >= 1)
        
        trend_plugin = self.engine.loader.get_plugin("cap_meth_trend_core")
        self.assertIsNotNone(trend_plugin)
        self.assertEqual(trend_plugin.version, "1.0.0")

    def test_full_pipeline_trace_and_metrics(self):
        market_state = MarketStateDTO(
            symbol="BTC-USD",
            timeframe="1H",
            features=FeatureSetDTO(features={"SMA_20": 50000.0, "SMA_50": 49000.0, "RSI_14": 65.0}),
            concepts=ConceptSetDTO(concepts={}),
            context=ExecutionContext(timestamp="2026-07-05T00:00:00Z", environment="test", run_id="run-123")
        )
        
        # Run 1: Should execute full pipeline
        results_1, traces_1 = self.engine.evaluate_all(market_state)
        
        # Run 2: Should hit cache
        results_2, traces_2 = self.engine.evaluate_all(market_state)
        
        # 1. Determinism
        self.assertEqual(len(results_1), len(results_2))
        self.assertEqual(results_1[0].confidence, results_2[0].confidence)
        
        # 2. Execution Trace Validation
        trace = traces_1[0]
        self.assertEqual(trace.plugin_id, "cap_meth_trend_core")
        self.assertEqual(trace.result, "SUCCESS")
        self.assertIn("Execution_Passed", trace.stages_executed)
        self.assertIn("Builders_Passed", trace.stages_executed)
        
        trace2 = traces_2[0]
        self.assertIn("Cache_Miss", trace.stages_executed)
        
        # 3. Metrics Validation
        metrics = self.engine.metrics.get_metrics()
        self.assertEqual(metrics.methodologies_executed, 1) # Second run was cached
        self.assertEqual(metrics.cache_hits, 1)
        self.assertEqual(metrics.success_rate, 1.0)
        self.assertEqual(metrics.failure_rate, 0.0)

if __name__ == '__main__':
    unittest.main()
