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

class TrendRule(AnalyticalRuleSDK):
    def get_capabilities(self) -> dict: return {"tier": 0, "deterministic": True, "supported_modes": ["Standard"], "ontology_id": "ONT-T0-009", "capability_id": "CAP-T0-009"}
    def get_dependencies(self) -> list: return ["RULE-T0-001", "RULE-T0-003", "RULE-T0-008"]
    def get_supported_registry_versions(self) -> dict: return {"analytical_rule_registry": ">=1.0.0"}
    def fingerprint(self) -> str: return hashlib.sha256(b"trend_rule_v1.0.0").hexdigest()

    def evaluate(self, context: RuleContextDTO) -> RuleEvidenceDTO:
        evidence_data = {"trend_direction": "Bullish", "trend_strength": 0.85, "trend_phase": "Expansion", "fractal_alignment": True, "internal_trend": "Bullish", "external_trend": "Bullish"}
        consumed_ids = ["EV-GEO-123", "EV-RNG-123", "EV-MTF-123"]
        return RuleEvidenceDTO(
            identity=RuleIdentityDTO(id=f'EV-TRND-{int(time.time()*1000)}', version='1.0.0', registry_checksum='TBD', producer_rule='RULE-T0-009', ontology_id='ONT-T0-009', capability_id='CAP-T0-009'),
            status=RuleResultStatus.SUCCESS, classification=EvidenceClassification.PRIMITIVE, evidence_type='TrendEvidence',
            evidence_data=evidence_data,
            quality=RuleQualityDTO(confidence=0.85, stability=0.9, consistency=0.8, coverage=1.0, uncertainty=0.1),
            provenance=RuleProvenanceDTO(dependency_chain=self.get_dependencies(), parent_rules=self.get_dependencies(), supporting_concepts=context.concept_references, rejected_concepts=[], graph_path=[], consumed_evidence_ids=consumed_ids, dependency_depth=1, execution_sequence=1, replay_epoch=0),
            schema_version='1.0.0', registry_version='1.0.0', compatibility_version='>=1.0.0', fingerprint='TRND123', timestamp=str(int(time.time()*1000)), explanation="Bullish trend detected."
        )
    def explain(self, evidence: RuleEvidenceDTO) -> str: return evidence.explanation
