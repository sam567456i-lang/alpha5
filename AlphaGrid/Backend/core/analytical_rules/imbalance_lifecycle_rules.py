from Backend.core.evidence_dtos.imbalance_events import PartialFillEvent, FullFillEvent
from Backend.core.evidence_dtos.imbalance import ImbalanceLifecycleState

class ImbalanceLifecycleEngine:
    """
    CQRS Command/Lifecycle Engine.
    Answers "How does the object change?" based strictly on inbound facts (Events).
    """
    
    def process_event(self, event, imbalance_object):
        """Mutates the object state based on the inbound event fact."""
        
        if isinstance(event, PartialFillEvent):
            # Only update if this penetration is deeper than previous
            if event.fill_percent_observed > imbalance_object.fill_geometry.fill_percent:
                imbalance_object.fill_geometry.fill_percent = event.fill_percent_observed
                imbalance_object.fill_geometry.deepest_penetration = event.penetration_depth_observed
                imbalance_object.fill_geometry.filled_height = event.penetration_depth_observed
                imbalance_object.fill_geometry.remaining_height = imbalance_object.height - event.penetration_depth_observed
                
                # Check for first touch
                if imbalance_object.fill_geometry.first_touch is None:
                    imbalance_object.fill_geometry.first_touch = event.trigger_time
                imbalance_object.fill_geometry.last_touch = event.trigger_time
                
                # Lifecycle state decision
                if imbalance_object.fill_geometry.fill_percent >= 100.0:
                    imbalance_object.lifecycle_state = ImbalanceLifecycleState.FILLED
                elif imbalance_object.fill_geometry.fill_percent > 0.0:
                    imbalance_object.lifecycle_state = ImbalanceLifecycleState.ACTIVE
                    
        elif isinstance(event, FullFillEvent):
            imbalance_object.fill_geometry.fill_percent = 100.0
            imbalance_object.fill_geometry.deepest_penetration = imbalance_object.height
            imbalance_object.fill_geometry.filled_height = imbalance_object.height
            imbalance_object.fill_geometry.remaining_height = 0.0
            imbalance_object.fill_geometry.last_touch = event.trigger_time
            imbalance_object.lifecycle_state = ImbalanceLifecycleState.FILLED
            
        return imbalance_object
