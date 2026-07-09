from typing import Dict, Any, List
from Backend.core.interfaces.core_interfaces import ITelemetry
from Backend.core.analytical_rules.dto.telemetry_evidence_dto import MetricEvidenceDTO, HealthEvidenceDTO, TelemetryEvidenceDTO

class TelemetryEngine(ITelemetry):
    """
    Observability engine that emits telemetry as Evidence rather than unstructured logs.
    """
    def __init__(self):
        self.evidence_stream: List[TelemetryEvidenceDTO] = []
        
    def emit_metric(self, name: str, value: float, tags: Dict[str, str] = None):
        if tags is None: tags = {}
        ev = MetricEvidenceDTO(
            identity=None, metadata=None, provenance=None, classification=None, interpretation_level=None, validity_status=None, evidence_data={},
            component_name=tags.get("component", "system"),
            metric_name=name,
            metric_value=value,
            tags=tags
        )
        self.evidence_stream.append(ev)
        
    def emit_health(self, component: str, status: str, details: Dict[str, Any] = None):
        if details is None: details = {}
        ev = HealthEvidenceDTO(
            identity=None, metadata=None, provenance=None, classification=None, interpretation_level=None, validity_status=None, evidence_data={},
            component_name=component,
            status=status,
            error_count=details.get("errors", 0),
            details=details
        )
        self.evidence_stream.append(ev)
