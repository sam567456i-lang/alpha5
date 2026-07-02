"""Concept Engine for evaluating all registered concepts."""

import logging
from typing import Dict, Any, List
from datetime import datetime
from .registry import ConceptRegistry
from .base import Concept
from .generator import AbstractConceptGenerator

logger = logging.getLogger(__name__)


class ConceptEngine:
    """
    Evaluates all registered concepts per market event, consuming Feature outputs.
    """

    def __init__(self, registry: ConceptRegistry) -> None:
        self._registry = registry
        self._generators: List[AbstractConceptGenerator] = self._registry.get_all()

    def process(self, timestamp: datetime, feature_values: Dict[str, Any]) -> Dict[str, Concept]:
        """
        Evaluates all concepts given the current feature values.
        
        Args:
            timestamp: Event timestamp.
            feature_values: Dictionary of feature outputs.
            
        Returns:
            Dictionary mapping concept ID to immutable Concept instances.
        """
        concepts: Dict[str, Concept] = {}
        
        for generator in self._generators:
            cid = generator.get_id()
            
            # Check if required features are present and not None (warming up)
            can_evaluate = True
            for req in generator.get_required_features():
                if req not in feature_values or feature_values[req] is None:
                    can_evaluate = False
                    break
                    
            if not can_evaluate:
                continue
                
            try:
                concept = generator.evaluate(timestamp, feature_values)
                concepts[cid] = concept
            except Exception as e:
                logger.error(f"Concept generation failed for '{cid}': {e}")
                # Phase 8 Rule: Concept generation failure -> fail the experiment.
                raise RuntimeError(f"Concept generation failed for '{cid}'") from e
                
        return concepts
