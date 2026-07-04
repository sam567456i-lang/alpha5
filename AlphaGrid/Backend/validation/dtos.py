from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

@dataclass(frozen=True)
class ValidationContextDTO:
    """
    Immutable context passed to every validator during execution.
    """
    phase: str
    family: str
    git_commit: str
    registry_version: str
    dto_version: str
    config_version: str
    dataset: str
    evidence_directory: str
    workspace: str
    profile: str
    validation_version: str = "1.0.0"

@dataclass
class ValidatorResultDTO:
    """
    Standardized output from any validator execution.
    """
    id: str
    # States: PENDING, READY, RUNNING, PASS, FAIL, WARNING, SKIPPED, BLOCKED, CANCELLED, TIMEOUT
    status: str 
    reason: str = ""
    duration_ms: float = 0.0
    phase: str = ""
    family: str = ""
    start_time: str = ""
    end_time: str = ""
    cpu_utilization_percent: float = 0.0
    peak_heap_mb: float = 0.0
    peak_rss_mb: float = 0.0
    gc_collections: int = 0
    evidence_id: str = ""
    validator_version: str = "1.0.0"
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    artifacts: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    max_error: float = 0.0
    mean_error: float = 0.0
    summary: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "reason": self.reason,
            "duration_ms": self.duration_ms,
            "phase": self.phase,
            "family": self.family,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "cpu_utilization_percent": self.cpu_utilization_percent,
            "peak_heap_mb": self.peak_heap_mb,
            "peak_rss_mb": self.peak_rss_mb,
            "gc_collections": self.gc_collections,
            "evidence_id": self.evidence_id,
            "validator_version": self.validator_version,
            "warnings": self.warnings,
            "errors": self.errors,
            "artifacts": self.artifacts,
            "metrics": self.metrics,
            "max_error": self.max_error,
            "mean_error": self.mean_error,
            "summary": self.summary,
            "timestamp": self.timestamp
        }

@dataclass
class ValidationEvent:
    """
    Event streamed by the runner.
    Types: VALIDATION_STARTED, VALIDATOR_STARTED, VALIDATOR_PROGRESS, VALIDATOR_FINISHED, VALIDATION_FINISHED
    """
    event_type: str
    validator_id: Optional[str] = None
    progress_pct: Optional[float] = None
    result: Optional[ValidatorResultDTO] = None
    message: str = ""
