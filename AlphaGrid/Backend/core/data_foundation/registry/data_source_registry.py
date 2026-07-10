from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class DataSourceMetadata:
    """Explicitly declares the capabilities of an upstream data vendor."""
    provider_name: str
    supported_asset_classes: List[str]
    supported_resolutions: List[str]
    timezone: str
    corporate_action_policy: str # "ADJUSTED", "RAW", "MANUAL"
    tick_precision: int
    volume_semantics: str # "BASE", "QUOTE", "CONTRACTS"
    licensing: str
    version: str
    quality_score: float

class DataSourceRegistry:
    """Stores the vendor profiles so ingestion adapters don't hardcode capabilities."""
    def __init__(self):
        self._sources = {}
        
    def register_source(self, metadata: DataSourceMetadata):
        self._sources[metadata.provider_name] = metadata
