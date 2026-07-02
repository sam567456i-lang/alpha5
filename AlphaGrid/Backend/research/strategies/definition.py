"""Declarative Strategy Definition Contract."""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Type, Optional
import hashlib
import json
from Backend.features.base import AbstractFeature
from Backend.methodology.base import AbstractMethodology
from Backend.concepts.generator import AbstractConceptGenerator
from Backend.signals.primitive.base import AbstractPrimitiveSignalGenerator
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Backend.research.strategies.base_research_strategy import BaseResearchStrategy

@dataclass(frozen=True)
class ConceptDefinition:
    """Declarative definition for a Concept Generator."""
    generator_type: Type[AbstractConceptGenerator]
    source: str
    kwargs: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class PrimitiveSignalDefinition:
    """Declarative definition for a Primitive Signal Generator."""
    generator_type: Type[AbstractPrimitiveSignalGenerator]

@dataclass(frozen=True)
class StrategyDefinition:
    """
    StrategyDefinition Contract.
    
    A StrategyDefinition is purely declarative.
    It may contain: identifiers, feature references, concept references, primitive signal references, methodology references, parameters.
    It must never contain: instantiated runtime objects, mutable state, cached data, execution logic, evaluation logic.
    """
    id: str
    strategy_class: Type['BaseResearchStrategy']
    methodology: Type[AbstractMethodology]
    features: List[Type[AbstractFeature]]
    concepts: List[ConceptDefinition]
    primitive_signals: List[PrimitiveSignalDefinition]
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    # Traceability and Metadata Contract
    supported_asset_classes: List[str] = field(default_factory=list)
    supported_timeframes: List[str] = field(default_factory=list)
    research_hypothesis_id: Optional[str] = None
    schema_version: int = 1
    strategy_version: str = "1.0.0"

    def fingerprint(self) -> str:
        """
        Computes an immutable SHA256 fingerprint for the strategy.
        Ensures exact historical reproducibility.
        """
        # Collect deterministic string representations of dependencies
        feature_versions = [f"{f.get_name()}_{f.get_version()}" for f in self.features]
        
        # Sort for stable hashing
        feature_versions.sort()
        
        state = {
            "id": self.id,
            "strategy_version": self.strategy_version,
            "methodology": self.methodology.__name__,
            "features": feature_versions,
            "parameters": self.parameters
        }
        
        state_str = json.dumps(state, sort_keys=True)
        return hashlib.sha256(state_str.encode("utf-8")).hexdigest()
