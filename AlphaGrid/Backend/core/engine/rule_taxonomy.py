from abc import ABC, abstractmethod
from typing import Any

class Rule(ABC):
    @abstractmethod
    def evaluate(self, *args, **kwargs) -> Any: pass

class DetectionRule(Rule):
    """Detects the presence of a specific condition."""
    pass

class ClassificationRule(Rule):
    """Classifies an entity into a discrete category."""
    pass

class MeasurementRule(Rule):
    """Computes a continuous numeric value."""
    pass

class RelationshipRule(Rule):
    """Determines relationships between two entities."""
    pass

class AggregationRule(Rule):
    """Aggregates multiple entities into a composite."""
    pass

class TransformationRule(Rule):
    """Transforms data from one domain to another."""
    pass

class ValidationRule(Rule):
    """Validates structural correctness of inputs/outputs."""
    pass
