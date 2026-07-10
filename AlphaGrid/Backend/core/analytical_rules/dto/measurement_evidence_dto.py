from dataclasses import dataclass
from typing import Optional
from Backend.core.analytical_rules.dto.evidence_dto import EvidenceDTO

@dataclass(frozen=True)
class MeasurementEvidenceDTO(EvidenceDTO):
    """
    Standardized numerical measurement from Platform 10.
    Standardizes statistical confidence properties.
    """
    value: float
    unit: str
    confidence: float          # 0.0 to 1.0
    quality: float             # 0.0 to 1.0 (e.g. data quality)
    sample_size: int           # N used in calculation
    variance: Optional[float] = None
