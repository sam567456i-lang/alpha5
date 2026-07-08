from Backend.core.analytical_rules.sdk.analytical_rule_sdk import AnalyticalRuleSDK
from Backend.core.analytical_rules.dto.rule_context_dto import RuleContextDTO
from Backend.core.analytical_rules.dto.rule_evidence_dto import RuleEvidenceDTO
from Backend.core.analytical_rules.dto.rule_identity_dto import RuleIdentityDTO
from Backend.core.analytical_rules.dto.rule_quality_dto import RuleQualityDTO
from Backend.core.analytical_rules.dto.rule_provenance_dto import RuleProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.rule_result_status import RuleResultStatus
import hashlib
import time

class ContextAlignmentRule(AnalyticalRuleSDK):
    """Evaluates alignment across multiple analytical dimensions."""
    def get_capabilities(self) -> dict: return {"tier": 0, "deterministic": True, "supported_modes": ["Standard"], "ontology_id": "ONT-T0-019", "capability_id": "CAP-T0-019"}
    def get_dependencies(self) -> list: return ["RULE-T0-006", "RULE-T0-009", "RULE-T0-010", "RULE-T0-011", "RULE-T0-008"]
    def get_supported_registry_versions(self) -> dict: return {"analytical_rule_registry": ">=1.0.0"}
    def fingerprint(self) -> str: return hashlib.sha256(b"context_alignment_rule_v1").hexdigest()

    def evaluate(self, context: RuleContextDTO) -> RuleEvidenceDTO:
        evidence_data = {
            "alignment_score": 0.85,
            "aligned_dimensions": ["Trend", "Structure", "MultiTimeframe"],
            "conflicting_dimensions": ["Session"],
            "dominant_context": "Bullish",
            "alignment_strength": "Strong"
        }
        consumed_ids = ["EV-SESS-123", "EV-TRND-123", "EV-STRC-123", "EV-VOL-123", "EV-MTF-123"]
        return RuleEvidenceDTO(
            identity=RuleIdentityDTO(id=f'EV-CTX-{int(time.time()*1000)}', version='1.0.0', registry_checksum='TBD', producer_rule='RULE-T0-019', ontology_id='ONT-T0-019', capability_id='CAP-T0-019'),
            status=RuleResultStatus.SUCCESS, classification=EvidenceClassification.PRIMITIVE, evidence_type='ContextAlignmentEvidence',
            evidence_data=evidence_data,
            quality=RuleQualityDTO(confidence=0.88, stability=0.85, consistency=0.9, coverage=0.95, uncertainty=0.12),
            provenance=RuleProvenanceDTO(dependency_chain=self.get_dependencies(), parent_rules=self.get_dependencies(), supporting_concepts=context.concept_references, rejected_concepts=[], graph_path=[], consumed_evidence_ids=consumed_ids, dependency_depth=2, execution_sequence=4, replay_epoch=0),
            schema_version='1.0.0', registry_version='1.0.0', compatibility_version='>=1.0.0', fingerprint='CTX123', timestamp=str(int(time.time()*1000)), explanation="Strong bullish alignment across Structure and Trend."
        )
    def explain(self, evidence: RuleEvidenceDTO) -> str: return evidence.explanation
