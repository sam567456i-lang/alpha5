from typing import Dict, Optional, Callable
from Backend.core.evidence_dtos.base import BasePlatformObject, LifecycleState, InvalidationReason
from datetime import datetime

class LifecycleEvent(Enum):
    VALIDATE_REQUESTED = "VALIDATE_REQUESTED"
    CONFIRM_REQUESTED = "CONFIRM_REQUESTED"
    ACTIVATE_REQUESTED = "ACTIVATE_REQUESTED"
    TOUCH_REQUESTED = "TOUCH_REQUESTED"
    CONSUME_REQUESTED = "CONSUME_REQUESTED"
    STALE_REQUESTED = "STALE_REQUESTED"
    SUPERSEDE_REQUESTED = "SUPERSEDE_REQUESTED"
    ARCHIVE_REQUESTED = "ARCHIVE_REQUESTED"

class BaseObjectLifecycleEngine:
    """
    Generic lifecycle engine for all Platform 10 objects.
    Enforces rigid state transitions from CANDIDATE -> ARCHIVED.
    Centralized transition through event requests.
    """

    # Allowed transitions mapping a state to a list of allowed next states
    _ALLOWED_TRANSITIONS = {
        LifecycleState.CANDIDATE: [LifecycleState.DETECTED, LifecycleState.ARCHIVED],
        LifecycleState.DETECTED: [LifecycleState.VALIDATED, LifecycleState.ARCHIVED, LifecycleState.SUPERSEDED],
        LifecycleState.VALIDATED: [LifecycleState.CONFIRMED, LifecycleState.ARCHIVED, LifecycleState.SUPERSEDED, LifecycleState.STALE],
        LifecycleState.CONFIRMED: [LifecycleState.ACTIVE, LifecycleState.ARCHIVED, LifecycleState.SUPERSEDED, LifecycleState.STALE],
        LifecycleState.ACTIVE: [LifecycleState.TOUCHED, LifecycleState.CONSUMED, LifecycleState.SUPERSEDED, LifecycleState.ARCHIVED, LifecycleState.STALE],
        LifecycleState.TOUCHED: [LifecycleState.TOUCHED, LifecycleState.CONSUMED, LifecycleState.SUPERSEDED, LifecycleState.ARCHIVED, LifecycleState.STALE],
        LifecycleState.CONSUMED: [LifecycleState.ARCHIVED],
        LifecycleState.STALE: [LifecycleState.SUPERSEDED, LifecycleState.ARCHIVED],
        LifecycleState.SUPERSEDED: [LifecycleState.ARCHIVED],
        LifecycleState.ARCHIVED: []
    }
    
    _EVENT_TO_STATE_MAP = {
        LifecycleEvent.VALIDATE_REQUESTED: LifecycleState.VALIDATED,
        LifecycleEvent.CONFIRM_REQUESTED: LifecycleState.CONFIRMED,
        LifecycleEvent.ACTIVATE_REQUESTED: LifecycleState.ACTIVE,
        LifecycleEvent.TOUCH_REQUESTED: LifecycleState.TOUCHED,
        LifecycleEvent.CONSUME_REQUESTED: LifecycleState.CONSUMED,
        LifecycleEvent.STALE_REQUESTED: LifecycleState.STALE,
        LifecycleEvent.SUPERSEDE_REQUESTED: LifecycleState.SUPERSEDED,
        LifecycleEvent.ARCHIVE_REQUESTED: LifecycleState.ARCHIVED,
    }

    def __init__(self):
        # We can register callbacks for state changes if needed
        self.state_change_handlers: Dict[LifecycleState, Callable[[BasePlatformObject], None]] = {}

    def _can_transition(self, current_state: LifecycleState, new_state: LifecycleState) -> bool:
        return new_state in self._ALLOWED_TRANSITIONS.get(current_state, [])

    def process_event(self, obj: BasePlatformObject, event: LifecycleEvent, reason: InvalidationReason = InvalidationReason.NONE) -> bool:
        """
        Processes a lifecycle event request.
        """
        target_state = self._EVENT_TO_STATE_MAP.get(event)
        if not target_state:
            return False
            
        if not self._can_transition(obj.state, target_state):
            # In a production environment, this might raise a TransitionError
            return False
        
        # Use strictly encapsulated method to update state and bump revision
        obj._internal_set_state(target_state)
        obj.invalidation_reason = reason
        
        # Trigger any registered callbacks
        if target_state in self.state_change_handlers:
            self.state_change_handlers[target_state](obj)
            
        return True
