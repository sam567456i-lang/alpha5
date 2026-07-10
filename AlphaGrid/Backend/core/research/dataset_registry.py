from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime

class DatasetType(Enum):
    GOLDEN = "GOLDEN"
    BENCHMARK = "BENCHMARK"
    STRESS = "STRESS"
    REGRESSION = "REGRESSION"
    WALK_FORWARD = "WALK_FORWARD"
    PAPER_TRADING = "PAPER_TRADING"
    LIVE_REPLAY = "LIVE_REPLAY"

@dataclass(frozen=True)
class DataProvenance:
    """Immutable record tracking the exact lineage of a dataset."""
    vendor: str
    download_timestamp: datetime
    adjustments_applied: List[str] # e.g. ["SPLITS", "DIVIDENDS"]
    cleaning_pipeline_version: str
    timezone_calendar: str
    missing_data_policy: str
    corporate_action_version: str

@dataclass(frozen=True)
class DatasetMetadata:
    """Metadata tracking versioning and structure of a curated dataset."""
    dataset_id: str
    dataset_type: DatasetType
    provenance: DataProvenance
    symbols: List[str]
    start_time: datetime
    end_time: datetime
    resolution: str # e.g. "1m", "TICK"

class DatasetRegistry:
    """Central repository for loading and managing version-controlled datasets."""
    def __init__(self):
        self._datasets: Dict[str, DatasetMetadata] = {}
        
    def register_dataset(self, metadata: DatasetMetadata):
        self._datasets[metadata.dataset_id] = metadata
        
    def get_dataset(self, dataset_id: str) -> DatasetMetadata:
        if dataset_id not in self._datasets:
            raise KeyError(f"Dataset {dataset_id} not found in Registry.")
        return self._datasets[dataset_id]
