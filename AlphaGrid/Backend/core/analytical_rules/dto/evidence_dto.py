from dataclasses import dataclass
from typing import Any, Dict
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification

@dataclass(frozen=True)
class EvidenceDTO:
    """The abstract universal base for all evidence types."""
    identity: EvidenceIdentityDTO
    metadata: EvidenceMetadataDTO
    provenance: EvidenceProvenanceDTO
    classification: EvidenceClassification
    evidence_data: Dict[str, Any]
