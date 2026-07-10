from abc import ABC, abstractmethod
from typing import List, Dict, Any
from Backend.core.evidence_dtos.base import BasePlatformObject, QualityEvidence

class QualityRule(ABC):
    """
    Base class for individual quality rules.
    Each rule computes one specific dimension of QualityEvidence.
    """
    @abstractmethod
    def evaluate(self, obj: BasePlatformObject, context: Dict[str, Any]) -> float:
        pass

class FreshnessRule(QualityRule):
    def evaluate(self, obj: BasePlatformObject, context: Dict[str, Any]) -> float:
        # Example logic: inverse of age_bars, normalized
        age = context.get('age_bars', 0)
        return max(0.0, 1.0 - (age / 100.0))

class TouchCountRule(QualityRule):
    def evaluate(self, obj: BasePlatformObject, context: Dict[str, Any]) -> float:
        # Returns the raw touch count, or can normalize it
        return float(context.get('touch_count', 0))

class IntegrityRule(QualityRule):
    def evaluate(self, obj: BasePlatformObject, context: Dict[str, Any]) -> float:
        # E.g., based on how cleanly it was formed
        return float(context.get('integrity', 1.0))

class QualityPolicy:
    """
    A collection of QualityRules that defines how a specific type of object's
    multi-dimensional quality is assessed.
    """
    def __init__(self, rules: List[QualityRule]):
        self.rules = rules
        
    def evaluate_all(self, obj: BasePlatformObject, context: Dict[str, Any]) -> QualityEvidence:
        # For simplicity, we assume we have specific rules for each dimension
        # In a full implementation, rules would map to specific fields.
        return QualityEvidence(
            freshness=context.get('freshness', 1.0),
            integrity=context.get('integrity', 1.0),
            strength=context.get('strength', 1.0),
            touch_count=context.get('touch_count', 0),
            age_bars=context.get('age_bars', 0),
            timeframe_agreement=context.get('timeframe_agreement', 1.0),
            stability=context.get('stability', 1.0)
        )

class QualityEngine:
    """
    Executes QualityPolicies against BasePlatformObjects to publish QualityEvidence.
    Platform 10 never ranks objects; it only computes these objective dimensions.
    """
    def __init__(self):
        self.policies: Dict[str, QualityPolicy] = {}
        
    def register_policy(self, object_type: str, policy: QualityPolicy):
        self.policies[object_type] = policy
        
    def compute_quality(self, obj: BasePlatformObject, object_type: str, context: Dict[str, Any]) -> QualityEvidence:
        policy = self.policies.get(object_type)
        if not policy:
            raise ValueError(f"No QualityPolicy registered for {object_type}")
            
        quality = policy.evaluate_all(obj, context)
        obj.quality = quality
        return quality
