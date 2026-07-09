from dataclasses import dataclass, field
from typing import Dict, Any
from Backend.core.analytical_rules.dto.evidence_dto import EvidenceDTO

@dataclass(frozen=True)
class TelemetryEvidenceDTO(EvidenceDTO):
    """Base class for all telemetry-derived evidence."""
    component_name: str = ""

@dataclass(frozen=True)
class MetricEvidenceDTO(TelemetryEvidenceDTO):
    """Evidence of a specific quantitative metric (e.g. latency)."""
    metric_name: str = ""
    metric_value: float = 0.0
    tags: Dict[str, str] = field(default_factory=dict)

@dataclass(frozen=True)
class PerformanceEvidenceDTO(TelemetryEvidenceDTO):
    """Evidence of execution performance (e.g. CPU/Memory usage)."""
    cpu_usage_percent: float = 0.0
    memory_mb: float = 0.0
    execution_time_ms: float = 0.0

@dataclass(frozen=True)
class HealthEvidenceDTO(TelemetryEvidenceDTO):
    """Evidence of system or component health."""
    status: str = "HEALTHY" # HEALTHY, DEGRADED, FAILED
    error_count: int = 0
    details: Dict[str, Any] = field(default_factory=dict)
