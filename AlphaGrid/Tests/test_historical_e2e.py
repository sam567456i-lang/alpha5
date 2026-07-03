import pytest
import pandas as pd
from Backend.core.canonical_pipeline import DomainResearchPipeline
from Backend.market_intelligence.historical_market_pipeline import HistoricalMarketPipeline
from Backend.market_intelligence.providers.abstract_market_data_provider import HistoricalDataProvider
from Backend.market_intelligence.normalization_engine import NormalizationEngine
from Backend.market_intelligence.session_engine import SessionEngine
from Backend.market_intelligence.data_quality_gate import DataQualityGate
from Backend.features.engine import FeatureEngine
from Backend.features.registry import FeatureRegistry
from Tests.test_golden_pipeline import MockDependencyContainer, MockStrategyEngine, MockEvidenceEngine, ExperimentEngine, BacktestEngine, WalkForwardEngine, MonteCarloEngine, ResearchRegistry, CandidateRegistry, CanonicalValidationStrategy

def test_historical_e2e_pipeline():
    """
    Executes the golden pipeline using real historical data (if available) or 
    simulated dense data to test stability over thousands of bars.
    """
    # Use a dummy provider for scale, bypassing network to test pure engine scaling
    class ScalingProvider(HistoricalDataProvider):
        @property
        def provider_id(self) -> str: return "SCALING"
        @property
        def dataset_version(self) -> str: return "1.0"
        
        def get_historical_bars(self, symbol: str, start_time, end_time, timeframe: str) -> pd.DataFrame:
            # Generate 1000 bars
            bars = []
            base_ts = 1704067200000 # Jan 1 2024
            for i in range(1000):
                bars.append({
                    "timestamp": pd.to_datetime(base_ts + (i * 3600000), unit='ms').tz_localize('UTC'),
                    "open": 50000 + i,
                    "high": 50100 + i,
                    "low": 49900 + i,
                    "close": 50050 + i,
                    "volume": 100
                })
            df = pd.DataFrame(bars)
            df.set_index("timestamp", inplace=True)
            return df
            
    market_pipeline = HistoricalMarketPipeline(
        provider=ScalingProvider(),
        normalization_engine=NormalizationEngine(),
        session_engine=SessionEngine(),
        data_quality_gate=DataQualityGate()
    )
    feature_registry = FeatureRegistry()
    feature_engine = FeatureEngine(feature_registry)
    
    strategy = CanonicalValidationStrategy({})
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
    
    pipeline = DomainResearchPipeline(market_pipeline, feature_engine, container)
    expected_stages = [
        "Provider", "Normalization", "Session", "DataQuality", "PriceGeometry", 
        "Feature", "Concept", "Primitive", "Methodology", "Strategy", "Evidence",
        "Experiment", "Backtest", "WalkForward", "MonteCarlo", "ResearchRegistry", "CandidateRegistry",
        "Pipeline Health Report"
    ]
    manifest = {stage: {} for stage in expected_stages}
    
    # Execute Pipeline
    pipeline.execute("BTCUSDT", "1H", "2024-01-01", "2024-02-12", manifest=manifest)
    
    assert manifest["Pipeline Health Report"]["Status"] == "PASS"
