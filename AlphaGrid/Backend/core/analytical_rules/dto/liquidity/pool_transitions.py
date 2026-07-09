from dataclasses import dataclass
from enum import Enum
from Backend.core.analytical_rules.dto.liquidity.pool_state import PoolState

class PoolTransitionType(Enum):
    CREATED = "CREATED"
    UPDATED = "UPDATED"
    MERGED = "MERGED"
    SUPERSEDED = "SUPERSEDED"
    INVALIDATED = "INVALIDATED"
    ARCHIVED = "ARCHIVED"

@dataclass(frozen=True)
class PoolTransition:
    """
    State delta produced by the PoolLifecycleEngine representing a deterministic mutation of a pool state.
    """
    pool_id: str
    transition_type: PoolTransitionType
    previous_state: PoolState
    new_state: PoolState
    transition_reason: str
    trigger_event_id: str
