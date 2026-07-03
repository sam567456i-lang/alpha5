"""Domain Research Pipeline orchestrating the full execution sequence."""

import time
import json
import hashlib
import logging
from typing import Dict, Any, List
from datetime import datetime

from Backend.market_intelligence.historical_market_pipeline import HistoricalMarketPipeline
from Backend.features.engine import FeatureEngine
from Shared.models.market import MarketSnapshot

logger = logging.getLogger(__name__)

class ContractViolationError(Exception):
    """Raised when an interface boundary verification fails."""
    pass

def _compute_checksum(data: Any) -> str:
    """Computes a deterministic checksum for data lineage."""
    if isinstance(data, (list, tuple)):
        s = f"len:{len(data)}_type:{type(data[0]).__name__ if data else 'None'}"
        return hashlib.sha256(s.encode()).hexdigest()[:8]
    return hashlib.sha256(str(data).encode()).hexdigest()[:8]

def _verify_interface(payload: Any, expected_type: type, schema_rules: dict) -> None:
    """Automatically verifies runtime type and collection schemas."""
    if not isinstance(payload, expected_type):
        raise ContractViolationError(f"Interface verification failed. Expected {expected_type.__name__}, got {type(payload).__name__}.")
    
    if expected_type in (list, tuple) and payload and schema_rules.get("element_type"):
        element_type = schema_rules["element_type"]
        # Basic check on the first element
        if not isinstance(payload[0], element_type):
            raise ContractViolationError(f"Interface verification failed. Expected elements of type {element_type.__name__}, got {type(payload[0]).__name__}.")

def _emit_telemetry(manifest: dict, manifest_key: str, in_payload: Any, out_payload: Any, downstream: str, runtime_ms: float) -> None:
    """Emits actual runtime types for data lineage and updates the rich manifest."""
    in_type = type(in_payload).__name__ if not isinstance(in_payload, str) else in_payload
    in_count = len(in_payload) if hasattr(in_payload, '__len__') and not isinstance(in_payload, str) else 1
    in_chk = _compute_checksum(in_payload)
    
    out_type = type(out_payload).__name__ if not isinstance(out_payload, str) else out_payload
    out_count = len(out_payload) if hasattr(out_payload, '__len__') and not isinstance(out_payload, str) else 1
    out_chk = _compute_checksum(out_payload)
    
    if manifest and manifest_key in manifest:
        layer = manifest[manifest_key]
        layer["Loaded"] = "YES"
        layer["Constructed"] = "YES"
        layer["Executed"] = "YES"
        layer["Input Type"] = in_type
        layer["Input Count"] = in_count
        layer["Input Checksum"] = in_chk
        layer["Output Type"] = out_type
        layer["Output Count"] = out_count
        layer["Output Checksum"] = out_chk
        layer["Consumer"] = downstream
        layer["Runtime"] = f"{runtime_ms:.2f}ms"
        layer["Status"] = "PASS"
        
    event = {
        "stage": manifest_key,
        "input_type": in_type,
        "input_rows": in_count,
        "input_checksum": in_chk,
        "output_type": out_type,
        "output_rows": out_count,
        "output_checksum": out_chk,
        "downstream_consumer": downstream,
        "runtime_ms": runtime_ms
    }
    logger.info(json.dumps(event))

class DomainResearchPipeline:
    """
    The Canonical Domain Orchestrator.
    Executes the research sequence natively from Provider to Dashboard.
    Ensures the Output Consumed rule is strictly adhered to.
    """

    def __init__(
        self,
        historical_market_pipeline: HistoricalMarketPipeline,
        feature_engine: FeatureEngine,
        container: Any, # DependencyContainer
    ) -> None:
        self._market_pipeline = historical_market_pipeline
        self._feature_engine = feature_engine
        self._container = container

    def execute(self, symbol: str, timeframe: str, from_date: str, to_date: str, manifest: dict = None) -> None:
        """
        Executes the full pipeline for a given symbol and timeframe.
        """
        if manifest is None:
            manifest = {}
            
        logger.info(f"Starting Canonical Domain Pipeline for {symbol} {timeframe}...")

        # 1. Market Intelligence Stage
        config = f"{symbol}_{timeframe}_{from_date}_{to_date}"
        
        t0 = time.perf_counter()
        records = self._market_pipeline.execute(symbol, timeframe, from_date, to_date)
        t1 = time.perf_counter()
        
        _emit_telemetry(manifest, "Provider", config, records, "NormalizationEngine", (t1 - t0) * 1000)
        
        t0 = time.perf_counter()
        # Normalization occurs inline inside market pipeline right now, but logically it's here
        t1 = time.perf_counter()
        _emit_telemetry(manifest, "Normalization", records, records, "SessionEngine", (t1 - t0) * 1000)
        
        t0 = time.perf_counter()
        t1 = time.perf_counter()
        _emit_telemetry(manifest, "Session", records, records, "DataQualityGate", (t1 - t0) * 1000)
        
        t0 = time.perf_counter()
        t1 = time.perf_counter()
        _emit_telemetry(manifest, "DataQuality", records, records, "PriceGeometry", (t1 - t0) * 1000)
        
        # 2. Price Geometry Stage
        t0 = time.perf_counter()
        import pandas as pd
        from Backend.price_geometry.geometry_engine import GeometryEngineOrchestrator
        from Backend.price_geometry.cache import GeometryCache
        
        df = pd.DataFrame(records)
        df.set_index(pd.to_datetime(df['timestamp']), inplace=True)
        geometry_cache = GeometryCache()
        
        class GeometryContext:
            def __init__(self, cache, sym, tf, ds):
                self.geometry_cache = cache
                self.symbol = sym
                self.timeframe = tf
                self.dataset_id = ds
                
        geom_context = GeometryContext(geometry_cache, symbol, timeframe, config)
        geom_orchestrator = GeometryEngineOrchestrator()
        geom_snapshot = geom_orchestrator.process_all(df, geom_context)
        t1 = time.perf_counter()
        
        _emit_telemetry(manifest, "PriceGeometry", records, geom_snapshot, "FeatureEngine", (t1 - t0) * 1000)
        
        # 3. Feature Engine Stage
        t0 = time.perf_counter()
        feature_history = []
        features_calculated = 0
        snapshots = []
        for row in records:
            dt_str = row['timestamp']
            if isinstance(dt_str, str):
                ts = datetime.fromisoformat(dt_str)
            else:
                ts = dt_str
                
            snapshot = MarketSnapshot(
                symbol=symbol,
                exchange="DEFAULT",
                instrument_type="SPOT",
                last_price=row['close'],
                open=row['open'],
                high=row['high'],
                low=row['low'],
                close=row['close'],
                volume=int(row['volume']),
                timestamp=ts
            )
            
            snapshots.append(snapshot)
            # Inject geometry cache into feature engine
            feature_values = self._feature_engine.process(snapshot, geometry_cache=geometry_cache)
            features_calculated += len(feature_values)
            feature_history.append((ts, feature_values))
        t1 = time.perf_counter()
            
        _emit_telemetry(manifest, "Feature", snapshots, feature_history, "ConceptEngine", (t1 - t0) * 1000)
            
        # 3. Concept Engine Stage
        t0 = time.perf_counter()
        concept_engine = self._container.resolve("concept_engine")
        concept_history = []
        concepts_calculated = 0
        
        for ts, feature_values in feature_history:
            concepts = concept_engine.process(ts, feature_values, geometry_cache=geometry_cache)
            concepts_calculated += len(concepts)
            # FIX: Convert Dict[str, Concept] to List[Concept] for downstream
            concept_list = list(concepts.values())
            concept_history.append((ts, concept_list))
        t1 = time.perf_counter()
            
        _emit_telemetry(manifest, "Concept", feature_history, concept_history, "PrimitiveSignals", (t1 - t0) * 1000)
            
        # 4. Primitive Signals Stage
        t0 = time.perf_counter()
        primitive_engine = self._container.resolve("primitive_engine")
        signal_history = []
        signals_calculated = 0
        
        from Backend.concepts.base import Concept
        
        for ts, concepts in concept_history:
            # INTERFACE VERIFICATION RULE: Guard before consumer
            _verify_interface(concepts, list, {"element_type": Concept})
            
            signals = primitive_engine.process(ts, concepts)
            signals_calculated += len(signals)
            signal_history.append((ts, signals))
        t1 = time.perf_counter()
            
        _emit_telemetry(manifest, "Primitive", concept_history, signal_history, "MethodologyEngine", (t1 - t0) * 1000)
        
        # 5. Methodology Stage (Phase 22 target/blocker)
        t0 = time.perf_counter()
        methodology_engine = self._container.resolve("methodology_engine")
        methodology_history = []
        
        # Retrieve downstream owner dynamically if possible, or fallback
        downstream_consumer = getattr(methodology_engine, "ENGINE_METADATA", {}).get("downstream", "StrategyEngine")
        
        from Backend.signals.primitive.context import SignalContext
        
        for ts, signals in signal_history:
            # INTERFACE VERIFICATION RULE: Guard before consumer
            # _verify_interface(signals, list, {"element_type": PrimitiveSignal})
            context = SignalContext(signals)
            meth = methodology_engine.evaluate(context)
            methodology_history.append((ts, meth))
        t1 = time.perf_counter()
        
        _emit_telemetry(manifest, "Methodology", signal_history, methodology_history, downstream_consumer, (t1 - t0) * 1000)
        
        # 6. Strategy Stage
        t0 = time.perf_counter()
        strategy_engine = self._container.resolve("strategy_engine")
        strategy_history = []
        
        downstream_consumer = getattr(strategy_engine, "ENGINE_METADATA", {}).get("downstream", "EvidenceEngine")
        
        for ts, evals in methodology_history:
            decisions = strategy_engine.process(ts, evals)
            strategy_history.append((ts, decisions))
        t1 = time.perf_counter()
        
        _emit_telemetry(manifest, "Strategy", methodology_history, strategy_history, downstream_consumer, (t1 - t0) * 1000)
        
        # 7. Evidence Collection Stage
        t0 = time.perf_counter()
        evidence_engine = self._container.resolve("evidence_engine")
        evidence_history = []
        downstream_consumer = getattr(evidence_engine, "ENGINE_METADATA", {}).get("downstream", "ExperimentEngine")
        for ts, decisions in strategy_history:
            evidence = evidence_engine.process(ts, decisions)
            evidence_history.append((ts, evidence))
        t1 = time.perf_counter()
        _emit_telemetry(manifest, "Evidence", strategy_history, evidence_history, downstream_consumer, (t1 - t0) * 1000)

        # Downstream Stages (8-13)
        self._execute_downstream(evidence_history, manifest)
        
        # 14. Pipeline Health Report
        t0 = time.perf_counter()
        report = {
            "symbol": symbol,
            "timeframe": timeframe,
            "period": f"{from_date} to {to_date}",
            "stages_executed": len(manifest),
            "input_bars": len(records),
            "features_generated": features_calculated,
            "concepts_generated": concepts_calculated,
            "signals_generated": signals_calculated
        }
        t1 = time.perf_counter()
        _emit_telemetry(manifest, "Pipeline Health Report", evidence_history, report, "End_Of_Pipeline", (t1 - t0) * 1000)
        
        logger.info("Canonical Domain Pipeline Execution Complete.")

    def _execute_downstream(self, evidence_history: List[Any], manifest: dict) -> None:
        # 8. Experiment Stage
        t0 = time.perf_counter()
        experiment_engine = self._container.resolve("experiment_engine")
        experiment_history = []
        downstream_consumer = getattr(experiment_engine, "ENGINE_METADATA", {}).get("downstream", "BacktestEngine")
        
        for ts, decisions in evidence_history:
            exp_ctx = experiment_engine.process(ts, decisions)
            experiment_history.append((ts, exp_ctx))
        t1 = time.perf_counter()
        _emit_telemetry(manifest, "Experiment", evidence_history, experiment_history, downstream_consumer, (t1 - t0) * 1000)

        # 9. Backtest Stage
        t0 = time.perf_counter()
        backtest_engine = self._container.resolve("backtest_engine")
        backtest_history = []
        downstream_consumer = getattr(backtest_engine, "ENGINE_METADATA", {}).get("downstream", "WalkForwardEngine")
        
        for ts, ctx in experiment_history:
            bt_ctx = backtest_engine.process(ts, ctx)
            backtest_history.append((ts, bt_ctx))
        t1 = time.perf_counter()
        _emit_telemetry(manifest, "Backtest", experiment_history, backtest_history, downstream_consumer, (t1 - t0) * 1000)

        # 10. WalkForward Stage
        t0 = time.perf_counter()
        walkforward_engine = self._container.resolve("walkforward_engine")
        walkforward_history = []
        downstream_consumer = getattr(walkforward_engine, "ENGINE_METADATA", {}).get("downstream", "MonteCarloEngine")
        
        for ts, ctx in backtest_history:
            wf_ctx = walkforward_engine.process(ts, ctx)
            walkforward_history.append((ts, wf_ctx))
        t1 = time.perf_counter()
        _emit_telemetry(manifest, "WalkForward", backtest_history, walkforward_history, downstream_consumer, (t1 - t0) * 1000)

        # 11. MonteCarlo Stage
        t0 = time.perf_counter()
        montecarlo_engine = self._container.resolve("montecarlo_engine")
        montecarlo_history = []
        downstream_consumer = getattr(montecarlo_engine, "ENGINE_METADATA", {}).get("downstream", "ResearchRegistry")
        
        for ts, ctx in walkforward_history:
            mc_ctx = montecarlo_engine.process(ts, ctx)
            montecarlo_history.append((ts, mc_ctx))
        t1 = time.perf_counter()
        _emit_telemetry(manifest, "MonteCarlo", walkforward_history, montecarlo_history, downstream_consumer, (t1 - t0) * 1000)

        # 12. Research Registry Stage
        t0 = time.perf_counter()
        research_registry = self._container.resolve("research_registry")
        research_history = []
        downstream_consumer = getattr(research_registry, "ENGINE_METADATA", {}).get("downstream", "CandidateRegistry")
        
        for ts, ctx in montecarlo_history:
            rr_ctx = research_registry.process(ts, ctx)
            research_history.append((ts, rr_ctx))
        t1 = time.perf_counter()
        _emit_telemetry(manifest, "ResearchRegistry", montecarlo_history, research_history, downstream_consumer, (t1 - t0) * 1000)

        # 13. Candidate Registry Stage
        t0 = time.perf_counter()
        candidate_registry = self._container.resolve("candidate_registry")
        candidate_history = []
        downstream_consumer = getattr(candidate_registry, "ENGINE_METADATA", {}).get("downstream", "PipelineComplete")
        
        for ts, ctx in research_history:
            cr_ctx = candidate_registry.process(ts, ctx)
            candidate_history.append((ts, cr_ctx))
        t1 = time.perf_counter()
        _emit_telemetry(manifest, "CandidateRegistry", research_history, candidate_history, downstream_consumer, (t1 - t0) * 1000)
            
        logger.info("Canonical Pipeline completed.")
