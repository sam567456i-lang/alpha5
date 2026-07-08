from dataclasses import dataclass
from typing import Any, Dict
from Backend.core.analytical_rules.dto.evidence_dto import EvidenceDTO
from Backend.core.analytical_rules.dto.rule_result_status import RuleResultStatus
from Backend.core.analytical_rules.dto.rule_quality_dto import RuleQualityDTO

@dataclass(frozen=True)
class RuleEvidenceDTO(EvidenceDTO):
    """Legacy wrapper for Rule Evidence before state/event separation."""
    status: RuleResultStatus
    quality: RuleQualityDTO
    explanation: str
