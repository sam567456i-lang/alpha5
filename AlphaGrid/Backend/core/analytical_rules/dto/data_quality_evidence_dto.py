from dataclasses import dataclass
from Backend.core.analytical_rules.dto.evidence_dto import EvidenceDTO

@dataclass(frozen=True)
class DataQualityEvidenceDTO(EvidenceDTO):
    """Objective assessment of data quality from the TimeDomain."""
    symbol_id: str = ""
    coverage_percentage: float = 1.0
    missing_percentage: float = 0.0
    interpolation_percentage: float = 0.0
    latency_ms: float = 0.0
    revision_count: int = 0
    confidence_score: float = 1.0
    validity_status_flags: str = "PRISTINE" # PRISTINE, RECONSTRUCTED, INTERPOLATED, SYNTHETIC
