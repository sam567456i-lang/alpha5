from enum import Enum
from abc import ABC, abstractmethod
from typing import Any, Optional, Dict, List
from dataclasses import dataclass, field
from datetime import datetime
from Shared.dtos.execution_context import ExecutionContext
from Backend.shared_domain.contracts.dtos import LineageDTO

class StateLifecycle(Enum):
    CREATED = "CREATED"
    UPDATED = "UPDATED"
    SUPERSEDED = "SUPERSEDED"
    EXPIRED = "EXPIRED"
    ARCHIVED = "ARCHIVED"

@dataclass
class BaseState(ABC):
    context: ExecutionContext
    lifecycle: StateLifecycle
    timestamp: datetime
    version: int
    
    # State Lifecycle & Metrics
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime] = None
    
    # Three-Layer Confidence
    deterministic_confidence: float = 1.0
    statistical_confidence: float = 1.0
    final_confidence: float = 1.0
    
    quality: float = 1.0
    source: str = "unknown"
    lineage: Optional['LineageDTO'] = None
    
    # State Expiration Policy
    valid_until: Optional[datetime] = None
    expires_after: Optional[int] = None # in seconds or bars
    refresh_policy: str = "NEVER"
    stale_after: Optional[int] = None
    invalid_after: Optional[int] = None
    
    # State Dependency Graph (Required by v25 Project OS)
    consumes: List[str] = field(default_factory=list)
    produces: List[str] = field(default_factory=list)

    @classmethod
    @abstractmethod
    def calculate_next(cls, previous_state: Optional['BaseState'], input_dto: Any, context: ExecutionContext) -> 'BaseState':
        """
        Produce the next deterministic state transition.
        MUST NOT scan historical datastores. MUST be strictly incremental.
        """
        pass
    
    @abstractmethod
    def serialize(self) -> dict:
        pass

    @classmethod
    @abstractmethod
    def deserialize(cls, data: dict) -> 'BaseState':
        pass
