from dataclasses import dataclass

@dataclass
class RelationshipPolicy:
    """Configurable policy for cross-market analytics thresholds."""
    minimum_overlap: int = 100
    minimum_correlation: float = 0.5
    minimum_history: int = 200
    rolling_window: int = 20
    minimum_confidence: float = 0.7
