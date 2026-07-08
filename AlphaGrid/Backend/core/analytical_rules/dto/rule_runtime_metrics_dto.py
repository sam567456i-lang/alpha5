from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class RuleRuntimeMetricsDTO:
    """Telemetry for rule execution performance and behavior tracking."""
    total_execution_time_ms: float
    planner_time_ms: float
    rule_execution_time_ms: float
    batching_time_ms: float
    serialization_time_ms: float
    replay_time_ms: float
    evidence_count: int
    blocked_count: int
    skipped_count: int
    failed_count: int
    memory_allocations_kb: float
    cache_hits: int
