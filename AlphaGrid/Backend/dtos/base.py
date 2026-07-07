from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
from Shared.dtos.execution_context import ExecutionContext

class BaseObject(BaseModel):
    id: str
    schema_version: str = "1.0.0"
    owner: str
    producer: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Mandatory Execution Context replacing generic trace_ids
    execution_context: ExecutionContext
    
    fingerprint: str
    checksum: str
    quality: float = 1.0
    
    # Three-Layer Confidence (Replacing singular confidence)
    deterministic_confidence: float = 0.0
    statistical_confidence: float = 0.0
    final_confidence: float = 0.0
    
    lifecycle: str = "ACTIVE"
    tags: List[str] = Field(default_factory=list)
    lineage: Dict[str, Any] = Field(default_factory=dict)

class BaseStateObject(BaseObject):
    """Base class for all States, incorporating Dependency Graph and Expiration."""
    
    # State Expiration Policy
    valid_until: Optional[datetime] = None
    expires_after: Optional[str] = None  # e.g., "1_bar", "session_end"
    refresh_policy: Optional[str] = None
    stale_after: Optional[datetime] = None
    invalid_after: Optional[datetime] = None
    
    # State Dependency Graph
    consumes: List[str] = Field(default_factory=list)
    produces: List[str] = Field(default_factory=list)
