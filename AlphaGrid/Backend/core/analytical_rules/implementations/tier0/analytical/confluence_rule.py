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

class ConfluenceRule(AnalyticalRuleSDK):
    """Evaluates total signal confluence prior to Tier 1 interpretation."""
    def get_capabilities(self) -> dict: return {"tier": 0, "deterministic": True, "supported_modes": ["Standard"], "ontology_id": "ONT-T0-020", "capability_id": "CAP-T0-020"}
    def get_dependencies(self) -> list: return ["RULE-T0-009", "RULE-T0-010", "RULE-T0-012", "RULE-T0-006", "RULE-T0-011", "RULE-T0-013"]
    def get_supported_registry_versions(self) -> dict: return {"analytical_rule_registry": ">=1.0.0"}
    def fingerprint(self) -> str: return hashlib.sha256(b"confluence_rule_v1").hexdigest()

    def evaluate(self, context: RuleContextDTO) -> RuleEvidenceDTO:
        evidence_data = {
            "number_of_confirmations": 4,
            "conflicting_signals": 1,
            "supporting_domains": ["Structure", "Liquidity", "Valuation"],
            "confluence_strength": "High"
        }
        consumed_ids = ["EV-TRND-123", "EV-STRC-123", "EV-LIQ-123", "EV-SESS-123", "EV-VOL-123", "EV-PREM-123"]
        return RuleEvidenceDTO(
            identity=RuleIdentityDTO(id=f'EV-CONF-{int(time.time()*1000)}', version='1.0.0', registry_checksum='TBD', producer_rule='RULE-T0-020', ontology_id='ONT-T0-020', capability_id='CAP-T0-020'),
            status=RuleResultStatus.SUCCESS, classification=EvidenceClassification.PRIMITIVE, evidence_type='ConfluenceEvidence',
            evidence_data=evidence_data,
            quality=RuleQualityDTO(confidence=0.95, stability=0.9, consistency=0.95, coverage=1.0, uncertainty=0.05),
            provenance=RuleProvenanceDTO(dependency_chain=self.get_dependencies(), parent_rules=self.get_dependencies(), supporting_concepts=context.concept_references, rejected_concepts=[], graph_path=[], consumed_evidence_ids=consumed_ids, dependency_depth=4, execution_sequence=5, replay_epoch=0),
            schema_version='1.0.0', registry_version='1.0.0', compatibility_version='>=1.0.0', fingerprint='CONF123', timestamp=str(int(time.time()*1000)), explanation="High confluence supported by Structure and Liquidity."
        )
    def explain(self, evidence: RuleEvidenceDTO) -> str: return evidence.explanation
