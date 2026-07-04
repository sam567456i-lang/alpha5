import os
import unittest
import pandas as pd
from typing import Dict, Any

from Backend.platforms.analysis.contracts import AnalysisContext, AnalysisResult
from Backend.platforms.analysis.registry import RegistryLoader
from Backend.platforms.analysis.factory import AnalysisFactory, BaseAnalysis
from Backend.platforms.analysis.validators.contract_validator import ContractValidator
from Backend.platforms.analysis.pipeline import AnalysisPipeline
from Backend.platforms.analysis.engine import AnalysisEngine

TEST_REGISTRY = os.path.join(os.path.dirname(__file__), "test_registry.yaml")
TEST_CONTRACTS = os.path.join(os.path.dirname(__file__), "test_contracts.yaml")

class MockTrendAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        return AnalysisResult(
            score=0.85,
            raw_data=context.market_data,
            signals=[{"type": "Buy", "price": 100}]
        )

class MockInvalidAnalysis(BaseAnalysis):
    def execute(self, context: AnalysisContext) -> AnalysisResult:
        return AnalysisResult(
            score=1.5,
            raw_data=context.market_data,
            signals=[]
        )

class TestCore(unittest.TestCase):
    def setUp(self):
        import yaml
        reg_data = {
            "capabilities": [
                {"capability_id": "MOCK-TREND-001", "platform": "P05", "family": "Trend"}
            ]
        }
        with open(TEST_REGISTRY, "w") as f:
            yaml.dump(reg_data, f)
            
        con_data = {
            "analysis_contract": {
                "version": "1.0.0"
            }
        }
        with open(TEST_CONTRACTS, "w") as f:
            yaml.dump(con_data, f)
            
    def tearDown(self):
        if os.path.exists(TEST_REGISTRY):
            os.remove(TEST_REGISTRY)
        if os.path.exists(TEST_CONTRACTS):
            os.remove(TEST_CONTRACTS)

    def test_registry_loader(self):
        loader = RegistryLoader(TEST_REGISTRY)
        meta = loader.get_metadata("MOCK-TREND-001")
        self.assertEqual(meta.family, "Trend")
        
    def test_factory(self):
        loader = RegistryLoader(TEST_REGISTRY)
        factory = AnalysisFactory(loader)
        factory.register("MOCK-TREND-001", MockTrendAnalysis)
        impl = factory.create("MOCK-TREND-001")
        self.assertIsInstance(impl, MockTrendAnalysis)

    def test_pipeline_valid(self):
        validator = ContractValidator(TEST_CONTRACTS)
        pipeline = AnalysisPipeline(validator)
        context = AnalysisContext(
            market_data=pd.DataFrame({"close": [1, 2, 3]}),
            timeframe="1D"
        )
        analysis = MockTrendAnalysis()
        result = pipeline.run(analysis, context)
        self.assertEqual(result.score, 0.85)
        self.assertEqual(len(result.signals), 1)

    def test_pipeline_invalid_output(self):
        validator = ContractValidator(TEST_CONTRACTS)
        pipeline = AnalysisPipeline(validator)
        context = AnalysisContext(
            market_data=pd.DataFrame({"close": [1, 2, 3]}),
            timeframe="1D"
        )
        analysis = MockInvalidAnalysis()
        with self.assertRaisesRegex(ValueError, "Contract Violation: score 1.5 outside"):
            pipeline.run(analysis, context)

    def test_engine_end_to_end(self):
        validator = ContractValidator(TEST_CONTRACTS)
        pipeline = AnalysisPipeline(validator)
        
        class MockRegistry:
            def get_metadata(self, cid):
                return None
                
        loader = MockRegistry()
        factory = AnalysisFactory(loader)
        factory.register("MOCK-TREND-001", MockTrendAnalysis)
        
        # We also need a mock indicator engine
        engine = AnalysisEngine(factory, pipeline)
        context = AnalysisContext(
            market_data=pd.DataFrame({"close": [1, 2, 3]}),
            timeframe="1D"
        )
        results = engine.run_batch(["MOCK-TREND-001"], context)
        self.assertIn("MOCK-TREND-001", results)
        self.assertEqual(results["MOCK-TREND-001"].score, 0.85)

if __name__ == "__main__":
    unittest.main()
