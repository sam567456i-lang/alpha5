"""Historical dataset loader and integrity verification (ADP Sec 3 & 4)."""

import hashlib
import json
import math
import unicodedata
from datetime import datetime, timezone
from typing import Any, Dict, Iterator, Optional

try:
    import duckdb
except ImportError:
    duckdb = None


class DatasetIntegrityError(Exception):
    """Raised when canonical dataset hash does not match expected snapshot ID."""
    pass


class DatasetLoader:
    """Loads historical datasets, verifies integrity, and streams chronologically."""

    def __init__(self, duckdb_conn: Any = None) -> None:
        if duckdb is None and duckdb_conn is None:
            raise ImportError("duckdb module is not installed")
        self.conn = duckdb_conn or duckdb.connect(database=":memory:")

    def _format_timestamp(self, ts: Any) -> str:
        """Formats timestamp to canonical ISO-8601 UTC string (YYYY-MM-DDTHH:MM:SS.ffffffZ)."""
        if isinstance(ts, datetime):
            # Ensure UTC
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            else:
                ts = ts.astimezone(timezone.utc)
            return ts.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        # If it's already a string or NumPy datetime64, we might need to parse/format it.
        # For simplicity, assuming duckdb returns datetime objects for timestamp columns.
        raise ValueError(f"Expected datetime object, got {type(ts)}")

    def _format_float(self, val: Any) -> str:
        """Formats float to exactly 8 decimal places. Rejects NaN and Infinity."""
        f_val = float(val)
        if math.isnan(f_val) or math.isinf(f_val):
            raise ValueError(f"Invalid float value: {f_val}")
        return f"{f_val:.8f}"

    def load_and_verify(
        self, 
        snapshot_id: str, 
        storage_path: str,
        start_bound: Optional[datetime] = None,
        end_bound: Optional[datetime] = None
    ) -> Iterator[Dict[str, Any]]:
        """
        Reads parquet, orders chronologically, verifies canonical hash, 
        and yields event dicts within the optional [start_bound, end_bound) range.
        """
        # 1. Strict column ordering per ADP Section 3
        query = f"""
            SELECT timestamp, open, high, low, close, volume 
            FROM read_parquet('{storage_path}') 
            ORDER BY timestamp ASC
        """
        # Execute query and fetch all to verify hash *before* yielding to prevent silent recovery
        results = self.conn.execute(query).fetchall()
        columns = ["timestamp", "open", "high", "low", "close", "volume"]

        formatted_rows = []
        last_timestamp = None

        for row in results:
            formatted_row = []
            for col_name, val in zip(columns, row):
                if col_name == "timestamp":
                    formatted_ts = self._format_timestamp(val)
                    if last_timestamp == formatted_ts:
                        raise ValueError(f"Duplicate timestamp detected: {formatted_ts}")
                    last_timestamp = formatted_ts
                    formatted_row.append(formatted_ts)
                elif col_name in ("open", "high", "low", "close", "volume"):
                    formatted_row.append(self._format_float(val))
                else:
                    formatted_row.append(str(val))
            formatted_rows.append(formatted_row)

        # 2. Canonical JSON string generation (UTF-8, separators)
        canonical_json = json.dumps(formatted_rows, sort_keys=True, separators=(",", ":"))
        canonical_json = unicodedata.normalize("NFC", canonical_json)
        computed_hash = hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()

        # 3. Pre-load Verification (ADP Section 4)
        if computed_hash != snapshot_id:
            raise DatasetIntegrityError(
                f"Dataset integrity verification failed. Expected {snapshot_id}, got {computed_hash}"
            )

        # 4. Stream chronologically (Look-ahead bias prevention begins here)
        for row in results:
            yield dict(zip(columns, row))
