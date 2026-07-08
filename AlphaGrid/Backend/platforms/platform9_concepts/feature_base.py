import os
from abc import ABC, abstractmethod
from typing import Any, Optional, Dict, List
from dataclasses import dataclass, field
from datetime import datetime

from Backend.core.state import ExecutionContext

@dataclass(frozen=True)
class FeatureType:
    id: str
    name: str
    family: str

@dataclass(frozen=True)
class BaseFeature(ABC):
    """
    Immutable representation of a Machine-Readable Feature.
    Must be created deterministically from immutable Analysis States.
    """
    context: ExecutionContext
    feature_id: str
    feature_type: FeatureType
    version: int
    
    # Quality & Confidence metrics derived from underlying states
    quality: float
    confidence: float
    produced_at: datetime
    
    # Explainability & Governance
    source_states: Dict[str, str] = field(default_factory=dict)
    
    # Lifecycle
    expires_at: Optional[datetime] = None
    
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    @abstractmethod
    def value(self) -> Any:
        """
        The machine-readable value of this feature.
        """
        pass

    def serialize(self) -> dict:
        return {
            "context": self.context.session_id,  # Simplified for serialization
            "feature_id": self.feature_id,
            "feature_type": self.feature_type.id,
            "version": self.version,
            "quality": self.quality,
            "confidence": self.confidence,
            "source_states": self.source_states,
            "produced_at": self.produced_at.isoformat() if self.produced_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "metadata": self.metadata,
            "value": self.value
        }

@dataclass(frozen=True)
class BooleanFeature(BaseFeature):
    feature_value: bool = False
    
    @property
    def value(self) -> bool:
        return self.feature_value

@dataclass(frozen=True)
class FloatFeature(BaseFeature):
    feature_value: float = 0.0
    
    @property
    def value(self) -> float:
        return self.feature_value
