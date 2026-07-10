from typing import Iterator, Dict, Any, Optional
import csv
from datetime import datetime, timezone
from dataclasses import dataclass
from Backend.core.data_foundation.contracts.schemas import OHLCSchema

@dataclass(frozen=True)
class CSVMapping:
    """Configurable column mapping for CSV adapters."""
    timestamp_col: str
    open_col: str
    high_col: str
    low_col: str
    close_col: str
    volume_col: str
    timestamp_format: str = "%Y-%m-%d %H:%M:%S"

class BaseIngestionAdapter:
    def ingest(self, source: Any) -> Iterator[OHLCSchema]:
        raise NotImplementedError

class CSVAdapter(BaseIngestionAdapter):
    """
    Reads CSV files, applies CSVMapping, and normalizes data to the canonical OHLCSchema.
    Strict Normalization:
    - Casts all numeric types to float
    - Forces all timestamps to strictly UTC timezone-aware
    - Handles NaNs (drops invalid numerical rows)
    """
    def __init__(self, mapping: CSVMapping):
        self.mapping = mapping
        self._seen_timestamps = set()

    def ingest(self, file_path: str) -> Iterator[OHLCSchema]:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Normalization: NaNs and missing fields
                    if not row.get(self.mapping.open_col) or not row.get(self.mapping.close_col):
                        continue

                    o = float(row[self.mapping.open_col])
                    h = float(row[self.mapping.high_col])
                    l = float(row[self.mapping.low_col])
                    c = float(row[self.mapping.close_col])
                    v = float(row[self.mapping.volume_col]) if row.get(self.mapping.volume_col) else 0.0

                    # Normalization: Timestamps and UTC
                    ts_raw = row[self.mapping.timestamp_col]
                    ts = datetime.strptime(ts_raw, self.mapping.timestamp_format)
                    if ts.tzinfo is None:
                        ts = ts.replace(tzinfo=timezone.utc)
                    else:
                        ts = ts.astimezone(timezone.utc)

                    yield OHLCSchema(
                        timestamp=ts,
                        open=o,
                        high=h,
                        low=l,
                        close=c,
                        volume=v,
                        optional_fields={}
                    )
                except (ValueError, KeyError):
                    # In a real implementation, we might log these skipped rows
                    continue
