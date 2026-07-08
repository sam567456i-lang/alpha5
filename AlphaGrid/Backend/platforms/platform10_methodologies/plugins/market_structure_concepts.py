"""
Platform 10: Concept Platform - Market Structure Concepts Plugin
Generates high-level market structure concepts from underlying features.
"""
from typing import List
from dataclasses import dataclass
from Backend.platforms.platform9_concepts.concept_base import (
    BaseConcept, ConceptID, ConceptCategory, ConceptType, ConceptSeverity
)
from Backend.platforms.platform9_concepts.concept_registry import ConceptPlugin, ConceptRegistry
from Backend.platforms.platform9_concepts.feature_base import BaseFeature
from Backend.core.state import ExecutionContext

@dataclass
class MarketRegimeConcept(BaseConcept):
    """Represents a specific market regime concept (e.g., Bull Market)."""
    regime_score: float = 0.0


@ConceptRegistry.register
class MarketStructureConceptPlugin(ConceptPlugin):
    """Plugin to extract market structure concepts from features."""
    
    @classmethod
    def get_category(cls) -> ConceptCategory:
        return ConceptCategory.STRUCTURE
        
    @classmethod
    def get_type(cls) -> ConceptType:
        return ConceptType.BULL_MARKET
        
    def extract(self, features: List[BaseFeature], context: ExecutionContext) -> List[BaseConcept]:
        """Extracts bull market concepts based on feature values."""
        concepts = []
        
        # Example logic: if we find a trend feature indicating strong upward movement, generate a concept
        # For this example, we'll just check if there's any feature and mock it up
        bullish_features = []
        for f in features:
            if hasattr(f, "value") and isinstance(f.value, (int, float)) and f.value > 0.5:
                bullish_features.append(f)
                
        if bullish_features:
            concept_id = ConceptID(
                category=self.get_category(),
                type=self.get_type()
            )
            concept = MarketRegimeConcept(
                concept_id=concept_id,
                source_features=bullish_features,
                description="Strong bullish market structure detected.",
                severity=ConceptSeverity.HIGH,
                confidence=0.85,
                context=context,
                regime_score=0.9
            )
            concepts.append(concept)
            
        return concepts
