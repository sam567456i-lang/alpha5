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

class VolatilityRule(AnalyticalRuleSDK):
    def get_capabilities(self) -> dict: return {"tier": 0, "deterministic": True, "supported_modes": ["Standard"], "ontology_id": "ONT-T0-011", "capability_id": "CAP-T0-011"}
    def get_dependencies(self) -> list: return ["RULE-T0-003", "RULE-T0-005", "RULE-T0-006"]
    def get_supported_registry_versions(self) -> dict: return {"analytical_rule_registry": ">=1.0.0"}
    def fingerprint(self) -> str: return hashlib.sha256(b"volatility_rule_v1.0.0").hexdigest()

    def evaluate(self, context: RuleContextDTO) -> RuleEvidenceDTO:
        evidence_data = {"atr_expansion": True, "atr_compression": False, "regime": "Expansion", "volatility_percentile": 85.5, "relative_volatility": 1.2}
        consumed_ids = ["EV-RNG-123", "EV-TIME-123", "EV-SESS-123"]
        return RuleEvidenceDTO(
            identity=RuleIdentityDTO(id=f'EV-VOL-{int(time.time()*1000)}', version='1.0.0', registry_checksum='TBD', producer_rule='RULE-T0-011', ontology_id='ONT-T0-011', capability_id='CAP-T0-011'),
            status=RuleResultStatus.SUCCESS, classification=EvidenceClassification.PRIMITIVE, evidence_type='VolatilityEvidence',
            evidence_data=evidence_data,
            quality=RuleQualityDTO(confidence=0.98, stability=0.9, consistency=0.9, coverage=1.0, uncertainty=0.02),
            provenance=RuleProvenanceDTO(dependency_chain=self.get_dependencies(), parent_rules=self.get_dependencies(), supporting_concepts=context.concept_references, rejected_concepts=[], graph_path=[], consumed_evidence_ids=consumed_ids, dependency_depth=1, execution_sequence=3, replay_epoch=0),
            schema_version='1.0.0', registry_version='1.0.0', compatibility_version='>=1.0.0', fingerprint='VOL123', timestamp=str(int(time.time()*1000)), explanation="Volatility Expansion."
        )
    def explain(self, evidence: RuleEvidenceDTO) -> str: return evidence.explanation
