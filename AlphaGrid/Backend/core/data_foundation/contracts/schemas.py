from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum
import hashlib
import json

class DataContractException(Exception):
    pass

class MarketType(Enum):
    CRYPTO = "CRYPTO"
    EQUITY = "EQUITY"
    INDEX = "INDEX"
    FUTURES = "FUTURES"
    FOREX = "FOREX"
    OPTIONS = "OPTIONS"

class GapPolicy(Enum):
    FAIL = "FAIL"
    WARN = "WARN"
    REPAIR = "REPAIR"

class DuplicatePolicy(Enum):
    FAIL = "FAIL"
    WARN = "WARN"
    REPAIR = "REPAIR"

class MissingVolumePolicy(Enum):
    FAIL = "FAIL"
    WARN = "WARN"
    REPAIR = "REPAIR"

class SplitPolicy(Enum):
    FAIL = "FAIL"
    WARN = "WARN"
    REPAIR = "REPAIR"

class DividendPolicy(Enum):
    FAIL = "FAIL"
    WARN = "WARN"
    REPAIR = "REPAIR"

class SymbolChangePolicy(Enum):
    FAIL = "FAIL"
    WARN = "WARN"
    REPAIR = "REPAIR"

class DelistingPolicy(Enum):
    FAIL = "FAIL"
    WARN = "WARN"
    REPAIR = "REPAIR"

@dataclass(frozen=True)
class ValidationProfile:
    """Strict rules for how to handle dirty data during ingestion."""
    name: str # e.g. "STRICT", "STANDARD", "FAST", "RESEARCH", "RAW"
    gap_policy: GapPolicy
    duplicate_policy: DuplicatePolicy
    split_policy: SplitPolicy
    dividend_policy: DividendPolicy
    symbol_change_policy: SymbolChangePolicy
    delisting_policy: DelistingPolicy
    missing_volume_policy: MissingVolumePolicy

@dataclass(frozen=True)
class OHLCSchema:
    """Explicit data contract for an OHLC bar."""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    optional_fields: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class TickSchema:
    """Explicit data contract for raw tick data. Future-proofed with optional fields."""
    timestamp: datetime
    price: float
    volume: Optional[float] = None
    bid: Optional[float] = None
    ask: Optional[float] = None
    bid_size: Optional[float] = None
    ask_size: Optional[float] = None
    trade_id: Optional[str] = None
    exchange: Optional[str] = None
    side: Optional[str] = None # "BUY", "SELL", "UNKNOWN"

@dataclass(frozen=True)
class DatasetDefinition:
    """The immutable definition of a dataset."""
    dataset_id: str
    provider: str
    provider_version: str
    market: MarketType
    asset_type: str
    symbol: str
    exchange: str
    currency: str
    timezone: str
    calendar: str
    resolution: str
    adjustment_policy: str
    corporate_action_policy: str
    fill_policy: str
    validation_profile: str
    start: str
    end: str
    row_count: int
    schema_version: str
    compatibility_version: str
    dataset_hash: str

    def to_json(self) -> str:
        d = {k: (v.value if isinstance(v, Enum) else v) for k, v in self.__dict__.items()}
        return json.dumps(d, sort_keys=True)

@dataclass(frozen=True)
class DatasetLineage:
    """Tracks how a dataset was created to maintain provenance."""
    operation: str # e.g. "INGEST", "RESAMPLE", "MERGE"
    input_datasets: List[str] # List of parent dataset_hashes
    output_dataset: str # The resulting dataset_hash
    timestamp: str
    builder_version: str
    configuration_hash: str

@dataclass(frozen=True)
class DatasetManifest:
    """Metadata generated after a dataset is successfully built."""
    dataset_hash: str
    row_count: int
    missing_bars: int
    duplicate_bars: int
    quality_score: float
    first_timestamp: str
    last_timestamp: str
    largest_gap_seconds: float
    average_gap_seconds: float
    resolution: str
    timezone: str
    calendar: str
    market: str
    asset_type: str
    symbol: str
    provider: str
    compression: str
    partition_count: int
    storage_size_bytes: int
    checksum: str
    start: str
    end: str
    schema_version: str
    builder_version: str
    catalog_version: str
    storage_version: str
    generation_time: str
    quality_report: Optional['FeedQualityReport'] = None
    lineage: Optional[DatasetLineage] = None

    def to_json(self) -> str:
        # Simplistic serialization for this exercise
        return json.dumps({k: str(v) for k, v in self.__dict__.items()}, sort_keys=True)

@dataclass(frozen=True)
class QualityScore:
    """Multidimensional data quality score derived deterministically."""
    completeness: float
    consistency: float
    integrity: float
    chronology: float
    calendar: float
    duplicates: float
    normalization: float

    @property
    def overall_score(self) -> float:
        scores = [
            self.completeness, self.consistency, self.integrity, 
            self.chronology, self.calendar, self.duplicates, self.normalization
        ]
        return sum(scores) / len(scores)

@dataclass(frozen=True)
class FeedQualityReport:
    """The deterministic output of the validation engine."""
    dataset_id: str
    validation_profile: str
    errors: List[str]
    warnings: List[str]
    repairs_applied: int
    quality_score: QualityScore
    status: str # e.g. "ACCEPTED", "REJECTED", "REPAIRED"

    def to_json(self) -> str:
        return json.dumps({
            "dataset_id": self.dataset_id,
            "validation_profile": self.validation_profile,
            "errors": self.errors,
            "warnings": self.warnings,
            "repairs_applied": self.repairs_applied,
            "quality_score": self.quality_score.__dict__,
            "status": self.status
        }, sort_keys=True)

@dataclass(frozen=True)
class ReplayContext:
    """Immutable context carried by every yielded bar."""
    replay_session_id: str
    dataset_id: str
    manifest_hash: str
    partition_id: str
    sequence: int
    current_bar: int
    total_bars: int
    timestamp: str
