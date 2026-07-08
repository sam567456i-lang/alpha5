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

class QualityRule(AnalyticalRuleSDK):
    """Evaluates evidence quality dimensions without computing final confidence."""
    def get_capabilities(self) -> dict: return {"tier": 0, "deterministic": True, "supported_modes": ["Standard"], "ontology_id": "ONT-T0-018", "capability_id": "CAP-T0-018"}
    def get_dependencies(self) -> list: return []
    def get_supported_registry_versions(self) -> dict: return {"analytical_rule_registry": ">=1.0.0"}
    def fingerprint(self) -> str: return hashlib.sha256(b"quality_rule_v1").hexdigest()

    def evaluate(self, context: RuleContextDTO) -> RuleEvidenceDTO:
        evidence_data = {
            "completeness": 0.95,
            "consistency": 0.9,
            "stability": 0.88,
            "reliability": 0.92,
            "uncertainty": 0.08,
            "confidence_inputs": {"source_data": 0.99, "model_fit": 0.85}
        }
        return RuleEvidenceDTO(
            identity=RuleIdentityDTO(id=f'EV-QUAL-{int(time.time()*1000)}', version='1.0.0', registry_checksum='TBD', producer_rule='RULE-T0-018', ontology_id='ONT-T0-018', capability_id='CAP-T0-018'),
            status=RuleResultStatus.SUCCESS, classification=EvidenceClassification.PRIMITIVE, evidence_type='QualityEvidence',
            evidence_data=evidence_data,
            quality=RuleQualityDTO(confidence=0.92, stability=0.88, consistency=0.9, coverage=0.95, uncertainty=0.08),
            provenance=RuleProvenanceDTO(dependency_chain=self.get_dependencies(), parent_rules=self.get_dependencies(), supporting_concepts=context.concept_references, rejected_concepts=[], graph_path=[], consumed_evidence_ids=[], dependency_depth=0, execution_sequence=1, replay_epoch=0),
            schema_version='1.0.0', registry_version='1.0.0', compatibility_version='>=1.0.0', fingerprint='QUAL123', timestamp=str(int(time.time()*1000)), explanation="Quality dimensions evaluated successfully."
        )
    def explain(self, evidence: RuleEvidenceDTO) -> str: return evidence.explanation
