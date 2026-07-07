import copy
import time
import uuid
from typing import List, Dict, Any, Tuple
from Backend.Platform10.contracts.dtos import MarketStateDTO, MethodologyResultDTO, ExecutionTraceDTO
from Backend.Platform10.engine.loader import PluginLoader
from Backend.Platform10.engine.builders import ConfidenceEngine, EvidenceBuilder, ExplainabilityBuilder
from Backend.Platform10.engine.cache import ExecutionCache
from Backend.Platform10.engine.scheduler import MethodologyScheduler
from Backend.Platform10.engine.graph import DependencyGraph
from Backend.Platform10.engine.sandbox import MethodologySandbox, TimeoutException
from Backend.Platform10.engine.metrics import PlatformMetrics

class MethodologyEngine:
    """Platform 10 Methodology Engine - Full Orchestration (10-Point Spec)"""
    
    def __init__(self, registry_caps: List[Dict[str, Any]], plugins_dir: str):
        self.registry_caps_map = {cap["id"]: cap for cap in registry_caps if cap.get("entity_type") == "capability"}
        
        self.loader = PluginLoader(registry_caps)
        self.loader.discover_and_load(plugins_dir)
        
        self.cache = ExecutionCache()
        self.metrics = PlatformMetrics()
        
    def evaluate_all(self, market_state: MarketStateDTO) -> Tuple[List[MethodologyResultDTO], List[ExecutionTraceDTO]]:
        results = []
        traces = []
        plugins = self.loader.get_all_plugins()
        plugin_ids = [p.methodology_id for p in plugins]
        
        # 5. Dependency Graph Topological Sort
        sorted_ids = DependencyGraph.topological_sort(plugin_ids, self.registry_caps_map)
        
        # We process plugins in dependency order
        for cap_id in sorted_ids:
            plugin = self.loader.get_plugin(cap_id)
            cap_meta = self.registry_caps_map.get(cap_id)
            
            trace_stages = []
            
            try:
                start_time = time.time()
                
                # 3. Methodology Scheduler
                if not MethodologyScheduler.should_execute(market_state, cap_meta):
                    self.metrics.record_skip()
                    continue
                trace_stages.append("Scheduler_Passed")
                    
                # 4. Execution Cache Check
                cached = self.cache.get(cap_id, market_state)
                if cached:
                    self.metrics.record_cache_hit()
                    results.append(cached[0])
                    traces.append(cached[1])
                    continue
                trace_stages.append("Cache_Miss")
                
                # Input Validation
                if not market_state or not market_state.features:
                    raise ValueError("Invalid MarketStateDTO")
                trace_stages.append("Input_Validation_Passed")
                
                # Dependency Validation
                missing_features = [f for f in cap_meta.get("required_features", []) if f not in market_state.features.features]
                if missing_features:
                    raise ValueError(f"Missing required features: {missing_features}")
                trace_stages.append("Dependency_Validation_Passed")
                
                # Execution (Immutable Context + Sandbox)
                state_copy = copy.deepcopy(market_state)
                
                budget_ms = cap_meta.get("timeout_ms", 1000.0) # Default 1s budget
                
                # Execute inside the sandbox
                confidence_factors, raw_data = MethodologySandbox.execute_with_budget(
                    plugin.evaluate_factors, budget_ms, state_copy
                )
                trace_stages.append("Execution_Passed")
                
                # Builders
                evidence_dto = EvidenceBuilder.build_evidence(raw_data)
                conf_model = cap_meta.get("confidence_model", "LinearDecay")
                final_confidence = ConfidenceEngine.calculate_confidence(confidence_factors, conf_model)
                explainability_dto = ExplainabilityBuilder.build_explainability(evidence_dto, raw_data)
                trace_stages.append("Builders_Passed")
                
                duration_ms = (time.time() - start_time) * 1000
                execution_id = str(uuid.uuid4())
                
                # Result DTO
                result_dto = MethodologyResultDTO(
                    methodology_id=plugin.methodology_id,
                    version=plugin.version,
                    plugin_id=f"{plugin.methodology_id}_{plugin.version}",
                    execution_id=execution_id,
                    execution_context=market_state.context,
                    score=final_confidence * 1.0, 
                    confidence=final_confidence,
                    strength=1.0,
                    evidence=evidence_dto,
                    supporting_concepts=evidence_dto.supporting_concepts,
                    conflicting_concepts=evidence_dto.conflicting_concepts,
                    preconditions=cap_meta.get("required_market_states", []),
                    failure_reasons=[],
                    explainability=explainability_dto,
                    metadata={
                        "category": cap_meta.get("category"),
                        "Methodology Health": raw_data.get("Methodology Health", "Unknown"),
                        "TrendProfile": raw_data.get("TrendProfile"),
                        "Confidence Provenance": raw_data.get("Confidence Provenance")
                    },
                    execution_duration_ms=duration_ms,
                    validation_status="CERTIFIED"
                )
                
                # Execution Trace DTO
                trace_dto = ExecutionTraceDTO(
                    execution_id=execution_id,
                    plugin_id=plugin.methodology_id,
                    stages_executed=trace_stages,
                    dependencies_consumed=cap_meta.get("dependencies", []),
                    evidence_generated=evidence_dto,
                    confidence_factors=confidence_factors,
                    final_confidence=final_confidence,
                    execution_duration_ms=duration_ms,
                    result="SUCCESS"
                )
                
                # Cache and Record
                self.cache.set(cap_id, market_state, result_dto, trace_dto)
                self.metrics.record_success(duration_ms, final_confidence)
                
                results.append(result_dto)
                traces.append(trace_dto)
                
            except TimeoutException as e:
                self.metrics.record_failure()
                print(f"[TIMEOUT] Methodology {cap_id} exceeded resource budget: {e}")
            except Exception as e:
                is_dep = "Missing required features" in str(e)
                self.metrics.record_failure(is_dependency=is_dep)
                print(f"[ERROR] Methodology {cap_id} failed pipeline: {e}")
                
        return results, traces
