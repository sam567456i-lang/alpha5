from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
import uuid
from datetime import datetime

class LifecycleState(Enum):
    CANDIDATE = "CANDIDATE"
    DETECTED = "DETECTED"
    VALIDATED = "VALIDATED"
    CONFIRMED = "CONFIRMED"
    ACTIVE = "ACTIVE"
    TOUCHED = "TOUCHED"
    CONSUMED = "CONSUMED"
    STALE = "STALE"
    SUPERSEDED = "SUPERSEDED"
    ARCHIVED = "ARCHIVED"

class EventLifecycleState(Enum):
    FIRED = "FIRED"
    CONFIRMED = "CONFIRMED"
    CONSUMED = "CONSUMED"
    ARCHIVED = "ARCHIVED"

class InvalidationReason(Enum):
    NONE = "NONE"
    PRICE_TRADED_THROUGH = "PRICE_TRADED_THROUGH"
    HIGHER_QUALITY_OBJECT = "HIGHER_QUALITY_OBJECT"
    WINDOW_EXPIRED = "WINDOW_EXPIRED"
    FAILED_VALIDATION = "FAILED_VALIDATION"
    MANUAL_OVERRIDE = "MANUAL_OVERRIDE"

@dataclass(frozen=True)
class LineageRecord:
    platform: str
    family: str
    capability: str
    source_dto_uuids: List[str]
    source_rule_ids: List[str]
    source_engine_id: str
    parent_object_uuids: List[str]
    source_revision: str  # Updated to reference exact historical revision
    version: str
    replay_id: str
    timestamp: datetime

class RelationshipType(Enum):
    BELONGS_TO = "belongs_to"
    DERIVED_FROM = "derived_from"
    COMPUTED_FROM = "computed_from"
    REFERENCES = "references"
    CONTAINS = "contains"
    OVERLAPS = "overlaps"
    SUPERSEDES = "supersedes"
    CONFIRMS = "confirms"
    INVALIDATES = "invalidates"

class Cardinality(Enum):
    ONE_TO_ONE = "1:1"
    ONE_TO_MANY = "1:M"
    MANY_TO_ONE = "M:1"
    MANY_TO_MANY = "M:M"

@dataclass(frozen=True)
class ObjectRelationship:
    source_uuid: str
    target_uuid: str
    relationship_type: RelationshipType
    cardinality: Cardinality
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class QualityEvidence:
    freshness: float
    integrity: float
    strength: float
    touch_count: int
    age_bars: int
    timeframe_agreement: float
    stability: float

@dataclass(frozen=True)
class IntegrityEvidence:
    """Distinct from Quality. Objectively tracks structural graph health."""
    missing_parents: bool
    broken_references: bool
    invalid_uuids: bool
    relationship_errors: bool

@dataclass(frozen=True)
class TimeframeTracking:
    """Explicitly tracks multi-timeframe provenance to avoid ambiguity."""
    origin_timeframe: str
    computation_timeframe: str
    publication_timeframe: str

@dataclass
class PlatformIdentity:
    """Globally unique identity for all Platform Objects."""
    uuid: str = field(default_factory=lambda: str(uuid.uuid4()))
    calendar: str = ""
    session: str = ""
    trading_day: str = ""
    boundary: str = ""
    timeframe: str = ""
    symbol: str = ""
    replay_id: str = ""
    owner_family: str = ""

@dataclass(frozen=True)
class FamilyMetadata:
    """Immutable capability metadata exposed to the Knowledge Graph."""
    family_id: str
    family_name: str
    owner: str
    inputs: List[str]
    outputs: List[str]
    dependencies: List[str]
    consumers: List[str]
    data_requirements: List[str]
    streaming_support: bool
    replay_support: bool
    computational_complexity: str
    memory_complexity: str
    schema_version: str
    crl: int
    certification_status: str

@dataclass
class BaseEvidence:
    """Root class for all immutable measurement."""
    pass

@dataclass
class BasePlatformArtifact(BaseEvidence):
    """Constitutional contract for all Platform 10 capability families."""
    pass

@dataclass
class MeasurementArtifact(BasePlatformArtifact): pass

@dataclass
class RelationshipArtifact(BasePlatformArtifact): pass

@dataclass
class QualityArtifact(BasePlatformArtifact): pass

@dataclass
class LifecycleArtifact(BasePlatformArtifact): pass

@dataclass
class ObjectArtifact(BasePlatformArtifact): pass

@dataclass
class EventArtifact(BasePlatformArtifact): pass

@dataclass(frozen=True)
class SchemaVersion:
    major: int
    minor: int
    patch: int
    
    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

class MigrationAdapter:
    """Stub framework to upgrade historical snapshots safely without breaking replay."""
    @classmethod
    def migrate(cls, snapshot: 'BasePlatformSnapshot', target_schema: SchemaVersion) -> 'BasePlatformSnapshot':
        return snapshot

@dataclass(frozen=True)
class BasePlatformSnapshot:
    """Immutable, append-only historical snapshot for deterministic replay."""
    uuid: str
    analytical_revision: int
    operational_revision: int
    schema_version: SchemaVersion
    payload: Dict[str, Any]
    timestamp: datetime

@dataclass
class BasePlatformObject(ObjectArtifact):
    """
    The universal root class for all durable Platform 10 objects.
    Components are strictly segregated for Platform 11 consumption.
    """
    identity: PlatformIdentity
    lineage: LineageRecord
    _state: LifecycleState = field(default=LifecycleState.CANDIDATE, init=False) # Strict encapsulation
    _analytical_revision: int = field(default=1, init=False)
    _operational_revision: int = field(default=1, init=False)
    invalidation_reason: InvalidationReason = InvalidationReason.NONE
    quality: Optional[QualityEvidence] = None
    integrity: Optional[IntegrityEvidence] = None
    relationships: List[ObjectRelationship] = field(default_factory=list)
    timeframe_tracking: Optional[TimeframeTracking] = None
    extensions: Dict[str, Any] = field(default_factory=dict)

    @property
    def state(self) -> LifecycleState:
        return self._state

    @property
    def analytical_revision(self) -> int:
        return self._analytical_revision

    @property
    def operational_revision(self) -> int:
        return self._operational_revision

    def _internal_increment_analytical_revision(self):
        """Called only when source evidence, price, or boundaries mathematically change."""
        self._analytical_revision += 1
        self._operational_revision += 1

    def _internal_set_state(self, new_state: LifecycleState):
        """Called only by Lifecycle Engine. Changes operational revision only."""
        self._state = new_state
        self._operational_revision += 1

@dataclass
class BoundaryObject(BasePlatformObject):
    """
    Universal reusable primitive for all boundary-based families (Range, Session, Reference, Structure).
    Provides consistent mathematical properties for geometry mapping.
    """
    upper_bound: float = 0.0
    lower_bound: float = 0.0
    origin_timestamp: datetime = field(default_factory=datetime.now)

    @property
    def midpoint(self) -> float:
        return (self.upper_bound + self.lower_bound) / 2.0

    @property
    def width(self) -> float:
        return abs(self.upper_bound - self.lower_bound)

@dataclass
class BasePlatformEvent(EventArtifact):
    """
    Universal primitive for all Platform 10/11 analytical events.
    Records interaction between Price/Time and a Certified Object.
    """
    event_id: str
    event_type: str
    trigger_time: datetime
    trigger_evidence: Any # OHLC/Tick causing the event
    trigger_object_uuids: List[str]
    source_object_revisions: Dict[str, int]
    triggering_bar_timestamp: datetime
    confidence: float
    event_lifecycle: EventLifecycleState = EventLifecycleState.FIRED
    lineage: Optional[LineageRecord] = None
    relationships: List[ObjectRelationship] = field(default_factory=list)
    replay_metadata: Dict[str, Any] = field(default_factory=dict)

