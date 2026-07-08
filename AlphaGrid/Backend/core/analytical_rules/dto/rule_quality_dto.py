from dataclasses import dataclass

@dataclass(frozen=True)
class RuleQualityDTO:
    """Formalizes the stability, coverage, and uncertainty of the rule's output."""
    confidence: float
    stability: float
    consistency: float
    coverage: float
    uncertainty: float
