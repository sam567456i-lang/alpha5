import copy
from typing import Optional, Union, Dict

from Backend.core.analytical_rules.dto.regions.region_events import RegionDetectedEventDTO, RegionReferenceInteractionEventDTO, RegionReferenceType
from Backend.core.analytical_rules.dto.regions.region_state import RegionState, RegionLifecycleState
from Backend.core.analytical_rules.dto.regions.region_geometry import RegionGeometryDTO

class RegionLifecycleEngine:
    """
    Generic event-sourced state transition engine for bounded Regions.
    Mutates RegionState based on objective regional interactions.
    Replaces capability-specific engines (like ImbalanceLifecycleEngine) to avoid duplicate lifecycle logic.
    """
    
    def __init__(self):
        self.state_cache: Dict[str, RegionState] = {}
        
    def process_event(self, event: Union[RegionDetectedEventDTO, RegionReferenceInteractionEventDTO]) -> Optional[RegionState]:
        if isinstance(event, RegionDetectedEventDTO):
            return self._handle_region_detected(event)
        elif isinstance(event, RegionReferenceInteractionEventDTO):
            return self._handle_reference_interaction(event)
        return None

    def _handle_region_detected(self, event: RegionDetectedEventDTO) -> Optional[RegionState]:
        # Accepts any RegionType, not just FVG
        geometry = RegionGeometryDTO(
            bounds=event.bounds,
            width=event.width,
            area=event.bounds.height * event.width,
            geometry_fingerprint=f"FINGERPRINT-{event.identity.evidence_id}"
        )
        
        new_state = RegionState(
            identity=event.identity,
            metadata=event.metadata,
            provenance=event.provenance,
            classification=event.classification,
            interpretation_level=event.interpretation_level,
            validity_status=event.validity_status,
            evidence_data={},
            region_identity=event.region_identity,
            geometry=geometry,
            lifecycle_state=RegionLifecycleState.CREATED,
            remaining_height=event.bounds.height
        )
        
        self.state_cache[event.region_identity.region_id] = new_state
        return new_state
        
    def _handle_reference_interaction(self, event: RegionReferenceInteractionEventDTO) -> Optional[RegionState]:
        current_state = self.state_cache.get(event.region_identity.region_id)
        if not current_state:
            return None
            
        if current_state.lifecycle_state in [RegionLifecycleState.FULLY_FILLED, RegionLifecycleState.ARCHIVED, RegionLifecycleState.INVALIDATED]:
            return None
            
        new_lifecycle = current_state.lifecycle_state
        new_remaining_height = current_state.remaining_height
        
        if event.reference_type == RegionReferenceType.FILL_FULL:
            new_lifecycle = RegionLifecycleState.FULLY_FILLED
            new_remaining_height = 0.0
        elif event.reference_type == RegionReferenceType.FILL_PARTIAL:
            new_lifecycle = RegionLifecycleState.PARTIALLY_FILLED
            # In a real app we'd calculate actual remaining height based on interaction price vs bounds
            new_remaining_height = current_state.remaining_height / 2.0 
            
        new_state = RegionState(
            identity=current_state.identity,
            metadata=current_state.metadata,
            provenance=current_state.provenance,
            classification=current_state.classification,
            interpretation_level=current_state.interpretation_level,
            validity_status=current_state.validity_status,
            evidence_data=current_state.evidence_data,
            region_identity=current_state.region_identity,
            geometry=current_state.geometry,
            lifecycle_state=new_lifecycle,
            remaining_height=new_remaining_height,
            region_metadata=current_state.region_metadata
        )
        
        self.state_cache[event.region_identity.region_id] = new_state
        return new_state
