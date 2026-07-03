"""
Data Provenance Module.

Attaches and tracks provenance for every dataset moving through the pipeline.
Provenance guarantees exact reproducibility of research experiments.

Dependency Graph:
    Consumes: [Canonical OHLCV DataFrame]
    Produces: [Provenance-Annotated Dataset]
    Registry: MarketIntelligenceRegistry (Future)
    Downstream: DataQualityGate
    Owner: MarketIntelligenceTeam
"""

import hashlib
import pandas as pd
from typing import Dict, Any, Optional
from datetime import datetime, timezone
import json


class DataProvenanceTracker:
    """Tracks and attaches provenance metadata to market datasets."""

    @staticmethod
    def calculate_dataset_hash(df: pd.DataFrame) -> str:
        """
        Calculates a deterministic hash for the dataset content.
        
        Args:
            df (pd.DataFrame): The dataset to hash.
            
        Returns:
            str: SHA-256 hash of the dataset contents.
        """
        if df.empty:
            return hashlib.sha256(b"empty").hexdigest()
        
        # Serialize the index and values securely to a string, then hash
        # We round floats to prevent floating point instability in hashes
        serialized = pd.util.hash_pandas_object(df.round(4)).values.tobytes()
        return hashlib.sha256(serialized).hexdigest()

    @staticmethod
    def generate_provenance_metadata(
        df: pd.DataFrame,
        provider_id: str,
        dataset_version: str,
        normalization_version: str,
        cleaning_version: str
    ) -> Dict[str, Any]:
        """
        Generates standard provenance metadata for a dataset.
        
        Args:
            df (pd.DataFrame): The dataset.
            provider_id (str): ID of the data provider (e.g. 'YAHOO').
            dataset_version (str): The version of the raw dataset.
            normalization_version (str): Version of the normalizer used.
            cleaning_version (str): Version of the cleaning logic used.
            
        Returns:
            Dict[str, Any]: Provenance metadata payload.
        """
        content_hash = DataProvenanceTracker.calculate_dataset_hash(df)
        import_time = datetime.now(timezone.utc).isoformat()
        
        return {
            "provider_id": provider_id,
            "dataset_version": dataset_version,
            "normalization_version": normalization_version,
            "cleaning_version": cleaning_version,
            "import_time": import_time,
            "content_hash": content_hash,
            "row_count": len(df),
            "start_time": df.index.min().isoformat() if not df.empty else None,
            "end_time": df.index.max().isoformat() if not df.empty else None
        }

    @staticmethod
    def attach_provenance(
        df: pd.DataFrame,
        provider_id: str,
        dataset_version: str,
        normalization_version: str,
        cleaning_version: str
    ) -> pd.DataFrame:
        """
        Attaches provenance metadata to the dataframe's attrs.
        
        Args:
            df (pd.DataFrame): The dataset.
            provider_id (str): ID of the data provider.
            dataset_version (str): The version of the raw dataset.
            normalization_version (str): Version of the normalizer used.
            cleaning_version (str): Version of the cleaning logic used.
            
        Returns:
            pd.DataFrame: The dataset with `.attrs['provenance']` populated.
        """
        metadata = DataProvenanceTracker.generate_provenance_metadata(
            df, provider_id, dataset_version, normalization_version, cleaning_version
        )
        df.attrs['provenance'] = metadata
        return df
