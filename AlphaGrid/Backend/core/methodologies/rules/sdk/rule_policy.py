from enum import Enum

class RulePromotionState(Enum):
    RESEARCH = "RESEARCH"
    CANDIDATE = "CANDIDATE"
    VALIDATED = "VALIDATED"
    DEPRECATED = "DEPRECATED"

class RulePolicyEngine:
    """Manages the lifecycle state machine for atomic rules."""
    
    @staticmethod
    def assert_can_assemble_in_methodology(state: RulePromotionState):
        """Methodologies cannot consume unvalidated rules."""
        if state != RulePromotionState.VALIDATED:
            raise ValueError(f"Rule must be VALIDATED to enter Methodology Assembly. Current: {state}")
