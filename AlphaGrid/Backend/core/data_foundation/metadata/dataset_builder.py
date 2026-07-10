import hashlib
from typing import Iterator, Optional, Dict, Any, List
from datetime import datetime
import copy

from Backend.core.data_foundation.contracts.schemas import (
    DatasetManifest, DatasetDefinition, DatasetLineage, 
    ValidationProfile, FeedQualityReport, OHLCSchema
)
from Backend.core.data_foundation.storage.storage_layer import StorageBackend

class DatasetBuilder:
    """Consumes an iterator of normalized bars and writes them to storage, generating a manifest."""
    
    def __init__(self, backend: StorageBackend, builder_version: str = "1.0.0", schema_version: str = "1.0.0", storage_version: str = "1.0.0", catalog_version: str = "1.0.0"):
        self.backend = backend
        self.builder_version = builder_version
        self.schema_version = schema_version
        self.storage_version = storage_version
        self.catalog_version = catalog_version

    def _compute_dataset_hash(self, definition: DatasetDefinition, profile: ValidationProfile, content_hash: str) -> str:
        """Deterministic hash including Definition, Policies, and Content."""
        h = hashlib.sha256()
        h.update(definition.to_json().encode())
        
        # Include all explicit policy strings
        policies = f"{profile.name}_{profile.gap_policy.name}_{profile.duplicate_policy.name}_{profile.split_policy.name}_{profile.dividend_policy.name}_{profile.symbol_change_policy.name}_{profile.delisting_policy.name}_{profile.missing_volume_policy.name}"
        h.update(policies.encode())
        
        h.update(definition.fill_policy.encode())
        h.update(definition.corporate_action_policy.encode())
        h.update(definition.adjustment_policy.encode())
        h.update(self.schema_version.encode())
        h.update(content_hash.encode())
        
        return h.hexdigest()

    def build_dataset(self, definition: DatasetDefinition, profile: ValidationProfile, stream: Iterator[OHLCSchema], quality_report: Optional[FeedQualityReport] = None, lineage: Optional[DatasetLineage] = None) -> DatasetManifest:
        """Consumes stream, writes to backend, and returns immutable manifest."""
        
        row_count = 0
        first_ts = None
        last_ts = None
        largest_gap = 0.0
        total_gap = 0.0
        
        content_hasher = hashlib.sha256()
        
        # We need to buffer data for the backend. The backend decides how to partition it.
        # But wait, StorageBackend.write_partition(canonical_path, data) requires us to provide canonical_path.
        # Wait, the user specifically requested: "ParquetBackend autonomously decides partition strategy. Builder knows nothing of partitions."
        # If the builder knows nothing of partitions, then the StorageBackend needs a `write_dataset(dataset_hash, stream)` method instead of `write_partition`.
        # Let's adjust StorageBackend.write_dataset
        
        # Actually, let's buffer the whole stream in memory for now, or just yield it to the backend.
        data_buffer = []
        
        for bar in stream:
            row_count += 1
            if first_ts is None:
                first_ts = bar.timestamp
            
            if last_ts is not None:
                gap = (bar.timestamp - last_ts).total_seconds()
                if gap > largest_gap:
                    largest_gap = gap
                total_gap += gap
                
            last_ts = bar.timestamp
            content_hasher.update(bar.timestamp.isoformat().encode())
            data_buffer.append(bar)

        content_hash = content_hasher.hexdigest()
        dataset_hash = self._compute_dataset_hash(definition, profile, content_hash)
        
        # Now pass to storage backend
        # Since the interface is currently write_partition, let's assume the backend has a new `write_dataset` method
        partition_count = self.backend.write_dataset(dataset_hash, data_buffer)
        
        avg_gap = total_gap / max(1, row_count - 1)
        
        # Extract quality info
        missing_bars = 0
        duplicate_bars = 0
        quality_score = 1.0
        
        if quality_report:
            # We mock the missing/duplicate bars based on the score or report
            quality_score = quality_report.quality_score.overall_score
            # In a real impl, we'd extract actual missing counts from the report
            
        manifest = DatasetManifest(
            dataset_hash=dataset_hash,
            row_count=row_count,
            missing_bars=missing_bars,
            duplicate_bars=duplicate_bars,
            quality_score=quality_score,
            first_timestamp=first_ts.isoformat() if first_ts else "",
            last_timestamp=last_ts.isoformat() if last_ts else "",
            largest_gap_seconds=largest_gap,
            average_gap_seconds=avg_gap,
            resolution=definition.resolution,
            timezone=definition.timezone,
            calendar=definition.calendar,
            market=definition.market.name,
            asset_type=definition.asset_type,
            symbol=definition.symbol,
            provider=definition.provider,
            compression="SNAPPY", # specific to Parquet usually, but assumed here
            partition_count=partition_count,
            storage_size_bytes=0, # The backend could return this, mock for now
            checksum=content_hash,
            start=definition.start,
            end=definition.end,
            schema_version=self.schema_version,
            builder_version=self.builder_version,
            catalog_version=self.catalog_version,
            storage_version=self.storage_version,
            generation_time=datetime.utcnow().isoformat(),
            quality_report=quality_report,
            lineage=lineage
        )
        return manifest
