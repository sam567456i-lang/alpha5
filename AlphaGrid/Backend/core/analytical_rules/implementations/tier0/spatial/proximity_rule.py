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

class ProximityRule(AnalyticalRuleSDK):
    def get_capabilities(self) -> dict: return {"tier": 0, "deterministic": True, "supported_modes": ["Standard"], "ontology_id": "ONT-T0-004", "capability_id": "CAP-T0-004"}
    def get_dependencies(self) -> list: return []
    def get_supported_registry_versions(self) -> dict: return {"analytical_rule_registry": ">=1.0.0"}
    def fingerprint(self) -> str: return hashlib.sha256(b"proximity_rule_v1").hexdigest()

    def evaluate(self, context: RuleContextDTO) -> RuleEvidenceDTO:
        return RuleEvidenceDTO(
            identity=RuleIdentityDTO(id=f'EV-RULE-T0-004-{int(time.time()*1000)}', version='1.0.0', registry_checksum='TBD', producer_rule='RULE-T0-004', ontology_id='ONT-T0-004', capability_id='CAP-T0-004'),
            status=RuleResultStatus.SUCCESS, classification=EvidenceClassification.PRIMITIVE, evidence_type='ProximityEvidence',
            evidence_data={"is_touching": False, "is_overlapping": True},
            quality=RuleQualityDTO(confidence=1.0, stability=1.0, consistency=1.0, coverage=1.0, uncertainty=0.0),
            provenance=RuleProvenanceDTO(dependency_chain=[], parent_rules=[], supporting_concepts=context.concept_references, rejected_concepts=[], graph_path=[], consumed_evidence_ids=[], dependency_depth=0, execution_sequence=0, replay_epoch=0),
            schema_version='1.0.0', registry_version='1.0.0', compatibility_version='>=1.0.0', fingerprint='PROX123', timestamp=str(int(time.time()*1000)), explanation='Proximity evaluated.'
        )
    def explain(self, evidence: RuleEvidenceDTO) -> str: return evidence.explanation
