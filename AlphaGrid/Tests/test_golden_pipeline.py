import pytest
from datetime import datetime, timedelta, timezone

from Backend.core.canonical_pipeline import DomainResearchPipeline
from Backend.market_intelligence.historical_market_pipeline import HistoricalMarketPipeline
from Backend.features.engine import FeatureEngine
from Backend.features.registry import FeatureRegistry

from Backend.research.engine.experiment_engine import ExperimentEngine
from Backend.research.engine.backtest_engine import BacktestEngine
from Backend.research.engine.walkforward_engine import WalkForwardEngine
from Backend.research.engine.montecarlo_engine import MonteCarloEngine
from Backend.research.repository.research_registry import ResearchRegistry
from Backend.research.repository.candidate_registry import CandidateRegistry

from Backend.research.strategies.canonical_validation import CanonicalValidationStrategy


class MockDependencyContainer:
    def __init__(self, bindings):
        self.bindings = bindings
    def resolve(self, key):
        return self.bindings[key]


class MockMarketPipeline(HistoricalMarketPipeline):
    def __init__(self):
        pass
    def execute(self, symbol, timeframe, from_date, to_date):
        # Generate some dummy OHLCV records
        base_time = datetime.fromisoformat("2026-01-01T00:00:00+00:00")
        records = []
        for i in range(100):
            records.append({
                "timestamp": (base_time + timedelta(hours=i)).isoformat(),
                "symbol": symbol,
                "open": 100 + i,
                "high": 105 + i,
                "low": 95 + i,
                "close": 102 + i,
                "volume": 1000
            })
        return records

class MockStrategyEngine:
    ENGINE_METADATA = {"downstream": "EvidenceEngine"}
    def process(self, timestamp, evaluations):
        return [{"timestamp": timestamp, "evals": evaluations, "decision": "MOCK"}]

class MockEvidenceEngine:
    ENGINE_METADATA = {"downstream": "ExperimentEngine"}
    def process(self, timestamp, decisions):
        return [{"timestamp": timestamp, "evidence": "MOCK_EVIDENCE"}]

def test_golden_pipeline_end_to_end():
    """
    Stage 0: Golden End-to-End Pipeline Test.
    Exercises the CanonicalValidationStrategy through all 15 stages.
    """
    market_pipeline = MockMarketPipeline()
    feature_engine = FeatureEngine(FeatureRegistry())
    
    # Initialize the Canonical Strategy which sets up its own internal engines
    # for Features, Concepts, Primitives, Methodologies, Signals, and Decisions.
    strategy = CanonicalValidationStrategy({})
    
    # Setup Dependency Container for downstream stages
    container = MockDependencyContainer({
        "concept_engine": strategy.concept_engine,
        "primitive_engine": strategy.primitive_signal_engine,
        "methodology_engine": strategy.methodology_engine,
        "strategy_engine": MockStrategyEngine(),
        "evidence_engine": MockEvidenceEngine(),
        "experiment_engine": ExperimentEngine(),
        "backtest_engine": BacktestEngine(),
        "walkforward_engine": WalkForwardEngine(),
        "montecarlo_engine": MonteCarloEngine(),
        "research_registry": ResearchRegistry(),
        "candidate_registry": CandidateRegistry()
    })
    
    pipeline = DomainResearchPipeline(
        historical_market_pipeline=market_pipeline,
        feature_engine=feature_engine,
        container=container
    )
    
    expected_stages = [
        "Provider", "Normalization", "Session", "DataQuality", "PriceGeometry", 
        "Feature", "Concept", "Primitive", "Methodology", "Strategy", "Evidence",
        "Experiment", "Backtest", "WalkForward", "MonteCarlo", "ResearchRegistry", "CandidateRegistry",
        "Pipeline Health Report"
    ]
    manifest = {stage: {} for stage in expected_stages}
    
    # Execute the Golden Pipeline
    try:
        pipeline.execute("BTCUSDT", "1H", "2026-01-01", "2026-01-10", manifest=manifest)
    except Exception as e:
        pytest.fail(f"Golden Pipeline crashed: {e}")
        
    # Verification: Assert all stages successfully executed
    expected_stages = [
        "Provider", "Normalization", "Session", "DataQuality", "PriceGeometry", 
        "Feature", "Concept", "Primitive", "Methodology", "Strategy", "Evidence",
        "Experiment", "Backtest", "WalkForward", "MonteCarlo", "ResearchRegistry", "CandidateRegistry",
        "Pipeline Health Report"
    ]
    
    for stage in expected_stages:
        assert stage in manifest, f"Stage '{stage}' completely missing from manifest telemetry!"
        if stage != "Pipeline Health Report":
            assert manifest[stage].get("Status") == "PASS", f"Stage '{stage}' did not emit PASS telemetry."
            assert manifest[stage].get("Output Count", 0) > 0, f"Stage '{stage}' produced 0 outputs!"
        else:
            assert manifest[stage].get("Status") == "PASS", f"Stage '{stage}' did not emit PASS telemetry."
