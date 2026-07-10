from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, TypeVar, Generic, List

# --- Identity & Checkpointing ---
@dataclass(frozen=True)
class ProfileIdentity:
    """Immutable identity tying a profile to its specific temporal/market bounds."""
    profile_uuid: str
    symbol: str
    timeframe: str
    window: str            # e.g., 'SESSION', 'DAILY', 'COMPOSITE'
    calendar: str
    binning_policy: str
    schema_version: str = "1.0.0"

@dataclass(frozen=True)
class ProfileSnapshot:
    """Immutable checkpoint containing the sparse histogram and computed states."""
    identity: ProfileIdentity
    histogram: Dict[float, float] # Price level -> Accumulation Value (Time or Volume)
    poc_price: float
    vah_price: float
    val_price: float
    metadata: Dict[str, Any] = field(default_factory=dict)

# --- Policies ---
@dataclass(frozen=True)
class POCPolicy:
    """Defines how the Point of Control is derived (e.g. handle ties)."""
    tie_breaker: str = "CLOSEST_TO_MID" # Other options: HIGHEST_PRICE, LOWEST_PRICE

@dataclass(frozen=True)
class ValueAreaPolicy:
    """Defines the Value Area expansion math."""
    value_area_pct: float = 0.68 # Institutional standard 68% (1 std dev)
    expansion_method: str = "SYMMETRIC" # Or VWAP_CENTERED

# --- Framework Interfaces ---
SampleT = TypeVar('SampleT') # Expected to be an immutable Bar or Tick

class BaseAccumulator(ABC, Generic[SampleT]):
    """
    Abstract interface for histogram aggregation.
    Can aggregate TPOs, Volume, Delta, or Footprints.
    """
    @abstractmethod
    def add(self, sample: SampleT) -> None:
        pass
        
    @abstractmethod
    def remove(self, sample: SampleT) -> None:
        pass
        
    @abstractmethod
    def merge(self, other: 'BaseAccumulator[SampleT]') -> None:
        pass
        
    @abstractmethod
    def snapshot(self, identity: ProfileIdentity) -> ProfileSnapshot:
        pass
        
    @abstractmethod
    def restore(self, snapshot: ProfileSnapshot) -> None:
        pass

class BaseProfileFramework(ABC, Generic[SampleT]):
    """
    Reusable infrastructure backbone managing streaming state, memory, and checkpointing.
    Delegates histogram logic to the injected Accumulator.
    """
    def __init__(self, identity: ProfileIdentity, accumulator: BaseAccumulator[SampleT]):
        self.identity = identity
        self.accumulator = accumulator
        self.snapshot_history: List[ProfileSnapshot] = []
        
    def process_sample(self, sample: SampleT) -> None:
        """Standardized streaming ingest."""
        self.accumulator.add(sample)
        
    def create_checkpoint(self) -> ProfileSnapshot:
        """O(1) immutable checkpointing for replay optimization."""
        snap = self.accumulator.snapshot(self.identity)
        self.snapshot_history.append(snap)
        return snap
        
    def restore_checkpoint(self, snapshot: ProfileSnapshot) -> None:
        """Instantly restores state from a checkpoint, skipping millions of tick replays."""
        if snapshot.identity.profile_uuid != self.identity.profile_uuid:
            raise ValueError("Identity mismatch on snapshot restore.")
        self.accumulator.restore(snapshot)
