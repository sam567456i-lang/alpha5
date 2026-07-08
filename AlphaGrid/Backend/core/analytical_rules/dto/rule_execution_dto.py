from dataclasses import dataclass

@dataclass(frozen=True)
class RuleExecutionDTO:
    """Tracks performance and operational telemetry (separated from semantic evidence)."""
    evaluation_time_ms: float
    memory_used_kb: float
    allocations: int
    cache_hits: int
    cache_misses: int
