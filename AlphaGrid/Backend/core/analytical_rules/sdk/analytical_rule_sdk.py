import abc
from Backend.core.analytical_rules.dto.rule_context_dto import RuleContextDTO
from Backend.core.analytical_rules.dto.rule_evidence_dto import RuleEvidenceDTO

class AnalyticalRuleSDK(abc.ABC):
    """
    The strict sandbox execution boundary for universal analytical rules.
    """
    
    @abc.abstractmethod
    def get_capabilities(self) -> dict:
        """Returns supported inputs, markets, modes, deterministic flags."""
        pass
        
    @abc.abstractmethod
    def get_dependencies(self) -> list:
        """Returns required prerequisite rules (prevents cycles)."""
        pass
        
    @abc.abstractmethod
    def get_supported_registry_versions(self) -> dict:
        """Returns registry compatibility ranges."""
        pass
        
    @abc.abstractmethod
    def fingerprint(self) -> str:
        """Returns a deterministic hash representing rule logic and version."""
        pass

    @abc.abstractmethod
    def evaluate(self, context: RuleContextDTO) -> RuleEvidenceDTO:
        """
        Executes the rule logic. 
        MUST be pure, stateless, and immutable.
        MUST ONLY return RuleEvidenceDTO.
        """
        pass

    @abc.abstractmethod
    def explain(self, evidence: RuleEvidenceDTO) -> str:
        """Transforms evidence into a human-readable explanation template."""
        pass
