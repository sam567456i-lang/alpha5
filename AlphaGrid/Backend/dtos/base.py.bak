from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

class BaseObject(BaseModel):
    id: str
    schema_version: str = "1.0.0"
    owner: str
    producer: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    trace_id: str
    correlation_id: str
    fingerprint: str
    checksum: str
    quality: float = 1.0
    confidence: float = 0.95
    lifecycle: str = "ACTIVE"
    tags: List[str] = Field(default_factory=list)
    lineage: Dict[str, Any] = Field(default_factory=dict)
