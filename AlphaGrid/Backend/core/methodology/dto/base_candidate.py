from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
import datetime

@dataclass(frozen=True)
class CandidateIdentity:
    """
    Provenance tracking for a Candidate.
    """
    id: str
    derived_from: str  # e.g., Evidence ID
    policy: str
    profile: str
    evaluation_id: Optional[str]
    sequence: int
    created_at: datetime.datetime

@dataclass(frozen=True)
class BaseCandidate:
    """
    Immutable, versioned, checksum-capable, replayable intermediate proposal.
    """
    identity: CandidateIdentity
    metadata: Dict[str, Any] = field(default_factory=dict)
    checksum: str = ""
    version: str = "1.0"

@dataclass(frozen=True)
class StructureCandidate(BaseCandidate):
    structure_type: str = ""

@dataclass(frozen=True)
class LiquidityCandidate(BaseCandidate):
    pool_id: str = ""

@dataclass(frozen=True)
class TargetCandidate(BaseCandidate):
    target_price: float = 0.0

@dataclass(frozen=True)
class SetupCandidate(BaseCandidate):
    setup_name: str = ""
    setup_direction: str = ""

@dataclass(frozen=True)
class EntryCandidate(BaseCandidate):
    entry_type: str = ""
    entry_price: float = 0.0
    stop_loss_price: float = 0.0
    target_price: float = 0.0
    fib_level: float = 0.0

@dataclass(frozen=True)
class DealingRangeCandidate(BaseCandidate):
    range_high: float = 0.0
    range_low: float = 0.0

@dataclass(frozen=True)
class PDArrayCandidate(BaseCandidate):
    array_type: str = ""
    classification: str = ""

@dataclass(frozen=True)
class RiskCandidate(BaseCandidate):
    risk_profile: str = ""

@dataclass(frozen=True)
class SessionCandidate(BaseCandidate):
    active_windows: List[str] = field(default_factory=list)

@dataclass(frozen=True)
class ConfluenceCandidate(BaseCandidate):
    component_candidate_ids: List[str] = field(default_factory=list)
    component_types: List[str] = field(default_factory=list)
    spatial_overlap: bool = False
    temporal_overlap: bool = False

@dataclass(frozen=True)
class SequenceCandidate(BaseCandidate):
    ordered_elements: List[str] = field(default_factory=list)
    ordering_constraints: List[str] = field(default_factory=list)
    maximum_gap: int = 0
    timeframe: str = ""
    sequence_window: str = ""
    derived_from: str = ""
    profile_identity: str = ""

@dataclass(frozen=True)
class CrossMarketCandidate(BaseCandidate):
    primary_symbol: str = ""
    secondary_symbol: str = ""
    primary_structure_state: str = ""
    secondary_structure_state: str = ""
    comparison_group: str = ""

@dataclass(frozen=True)
class AuctionCandidate(BaseCandidate):
    time_inside_region: int = 0
    volume_inside_region: float = 0.0
    rotation_count: int = 0
    region_type: str = ""
