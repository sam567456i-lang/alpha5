from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime

class ZoneLifecycleStatus(str, Enum):
    PENDING = "PENDING"
    DETECTED = "DETECTED"
    CONFIRMED = "CONFIRMED"
    ACTIVE = "ACTIVE"
    MITIGATED = "MITIGATED"
    INVALIDATED = "INVALIDATED"
    ARCHIVED = "ARCHIVED"

class ZonePresentationHint(str, Enum):
    FILLED = "FILLED"
    OUTLINED = "OUTLINED"
    HATCHED = "HATCHED"
    GRADIENT = "GRADIENT"
    HIDDEN = "HIDDEN"

@dataclass(frozen=True)
class ZoneIdentityDTO:
    """Immutable identity for a spatial zone."""
    zone_id: str
    zone_version: int
    previous_version_id: Optional[str]
    root_zone_id: str
    zone_type: str
    ontology_id: str
    capability_id: str
    market: str
    asset_class: str
    exchange: str
    symbol: str
    timeframe: str
    session_id: str
    source_detector: str
    registry_version: str

@dataclass(frozen=True)
class ZoneGeometryDTO:
    """Strictly physical spatial dimensions."""
    upper_price: float
    lower_price: float
    shape: str = "rectangle"  # Can support polygons, channels later
    centroid: Optional[float] = None
    width: Optional[float] = None  # Price width
    height: Optional[float] = None # Time height/duration
    area: Optional[float] = None
    orientation: Optional[float] = None

@dataclass(frozen=True)
class ZoneMetadataDTO:
    """Operational and tracking metadata."""
    registry_version: str
    fingerprint_hash: str
    created_by: str
    detector: str
    latency_ms: float
    confidence_model: str
    freshness_model: str
    schema_version: str = "1.0.0"
    
    # Replay Metadata
    replay_version: str = "1.0.0"
    replay_sequence: int = 0
    snapshot_generation: int = 0
    stream_generation: int = 0
    replay_epoch: int = 0

    # Evolution / Deprecation
    deprecated_by: Optional[str] = None
    superseded_by: Optional[str] = None
    replacement_zone_type: Optional[str] = None
    migration_notes: Optional[str] = None
    
    # Explainability
    confidence_contributors: Dict[str, float] = field(default_factory=dict)
    evidence_sources: List[str] = field(default_factory=list)
    supporting_objects: List[str] = field(default_factory=list)
    supporting_events: List[str] = field(default_factory=list)

    # Provenance Graph
    derived_from: List[str] = field(default_factory=list)
    merged_into: Optional[str] = None
    consumed_by: List[str] = field(default_factory=list)
    merge_history: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class ZoneDTO:
    """
    Unified spatial zone DTO. Behavior relies on registry and zone_type.
    No subclasses (e.g. no GapZoneDTO, BlockZoneDTO).
    """
    identity: ZoneIdentityDTO
    geometry: ZoneGeometryDTO
    metadata: ZoneMetadataDTO
    status: ZoneLifecycleStatus
    
    # Time Model
    created_at: datetime
    activated_at: Optional[datetime] = None
    confirmed_at: Optional[datetime] = None
    mitigated_at: Optional[datetime] = None
    invalidated_at: Optional[datetime] = None
    archived_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    
    # Confidence and Governance
    strength: float = 0.0
    freshness: float = 1.0
    
    # Visualization semantics
    presentation_hint: ZonePresentationHint = ZonePresentationHint.FILLED
    opacity: float = 0.5
    
    # Traceability
    lineage_ids: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class ZoneEventDTO:
    """Represents a discrete lifecycle event in the spatial event stream."""
    event_id: str
    zone_id: str
    event_type: str  # ZoneCreated, ZoneUpdated, ZoneMerged, ZoneSplit, etc.
    timestamp: datetime
    payload: Dict[str, Any]

