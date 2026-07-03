from typing import Dict, List, Optional
from Backend.concepts.core.objects import ConceptObject
from Backend.price_geometry.objects import LifecycleState

class ConceptLifecycleManager:
    """
    Tracks the validity of concepts as new geometry unfolds.
    For example, an Order Block is invalidated when its underlying FVG is filled
    or when price sweeps beyond its invalidation point.
    """
    def __init__(self) -> None:
        self._active_concepts: Dict[str, ConceptObject] = {}
        
    def add_concept(self, concept: ConceptObject) -> None:
        if concept.lifecycle_state == LifecycleState.CONFIRMED:
            self._active_concepts[concept.id] = concept
            
    def update_concept_state(self, concept_id: str, new_state: LifecycleState, mitigated_price: Optional[float] = None) -> None:
        if concept_id in self._active_concepts:
            concept = self._active_concepts[concept_id]
            object.__setattr__(concept, 'lifecycle_state', new_state)
            if mitigated_price is not None:
                if hasattr(concept, 'mitigated_price'):
                    object.__setattr__(concept, 'mitigated_price', mitigated_price)
                    
            if new_state in (LifecycleState.INVALIDATED, LifecycleState.BROKEN):
                # Optionally remove from active, or leave for historical query
                pass
                
    def get_active_concepts(self, concept_type: Optional[str] = None) -> List[ConceptObject]:
        active = [c for c in self._active_concepts.values() if c.lifecycle_state == LifecycleState.CONFIRMED]
        if concept_type:
            active = [c for c in active if c.concept_type == concept_type]
        return active
