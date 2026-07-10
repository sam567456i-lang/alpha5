from typing import Optional, List, Any
import json
from Backend.core.data_foundation.contracts.schemas import DatasetManifest
from Backend.core.data_foundation.metadata.dataset_catalog import DatasetCatalog, CatalogQuery
from Backend.core.data_foundation.storage.storage_layer import StorageBackend
from Backend.core.data_foundation.replay.sequential_replay import SequentialReplayEngine

class DatasetResolver:
    """Resolves specific dataset queries into DatasetManifests using the Catalog."""
    def __init__(self, catalog: DatasetCatalog):
        self.catalog = catalog
        
    def latest(self, symbol: str, resolution: str) -> Optional[DatasetManifest]:
        """Finds the most recently generated dataset for a given symbol and resolution."""
        q = CatalogQuery()
        q.symbol = symbol
        q.resolution = resolution
        
        matches = self.catalog.discover(q)
        if not matches:
            return None
            
        # Sort by generation_time descending
        matches.sort(key=lambda x: x.generation_time, reverse=True)
        return matches[0]

class DatasetLoader:
    """Seamlessly bridges a DatasetManifest into a ReplayEngine."""
    def __init__(self, storage: StorageBackend):
        self.storage = storage
        
    def load(self, manifest: DatasetManifest) -> SequentialReplayEngine:
        """Returns a ReplayEngine completely initialized. Replay does no searching."""
        return SequentialReplayEngine(manifest, self.storage)

class DatasetExporter:
    """Exports datasets to various formats for external research tools."""
    def __init__(self, storage: StorageBackend):
        self.storage = storage
        
    def export_csv(self, manifest: DatasetManifest, output_path: str):
        iterator = self.storage.read_dataset(manifest)
        import csv
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "open", "high", "low", "close", "volume"])
            for partition in iterator:
                for bar in partition:
                    writer.writerow([bar.timestamp, bar.open, bar.high, bar.low, bar.close, bar.volume])
                    
    def export_parquet(self, manifest: DatasetManifest, output_path: str):
        pass # Implementation for Parquet dump
        
    def export_duckdb(self, manifest: DatasetManifest, output_path: str):
        pass # Implementation for DuckDB dump

class DatasetInspector:
    """Generates detailed reports on a Dataset's health, lineage, and structure."""
    
    @staticmethod
    def generate_report(manifest: DatasetManifest) -> str:
        report = []
        report.append(f"=== Dataset Inspector Report ===")
        report.append(f"Hash: {manifest.dataset_hash}")
        report.append(f"Symbol: {manifest.symbol} | Resolution: {manifest.resolution}")
        report.append(f"Rows: {manifest.row_count} | Quality Score: {manifest.quality_score}")
        report.append(f"Partitions: {manifest.partition_count}")
        report.append(f"Time Range: {manifest.first_timestamp} to {manifest.last_timestamp}")
        
        if manifest.lineage:
            report.append("\n--- Lineage ---")
            report.append(f"Operation: {manifest.lineage.operation}")
            report.append(f"Input Datasets: {manifest.lineage.input_datasets}")
            report.append(f"Builder Version: {manifest.lineage.builder_version}")
            
        if manifest.quality_report:
            report.append("\n--- Validation Quality ---")
            report.append(f"Status: {manifest.quality_report.status}")
            report.append(f"Repairs: {manifest.quality_report.repairs_applied}")
            if manifest.quality_report.errors:
                report.append(f"Errors: {len(manifest.quality_report.errors)}")
                
        return "\n".join(report)
