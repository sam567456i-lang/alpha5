import numpy as np
from typing import Tuple

def sanitize_input(values: np.ndarray, timestamps: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Validates input arrays for strict institutional requirements.
    Enforces float64, size matching, and strictly monotonic timestamps.
    """
    if len(values) != len(timestamps):
        raise ValueError(f"Length mismatch: values ({len(values)}) != timestamps ({len(timestamps)})")
        
    values_64 = np.asarray(values, dtype=np.float64)
    timestamps_64 = np.asarray(timestamps, dtype=np.int64) # usually nanoseconds
    
    # Check monotonicity
    if not np.all(np.diff(timestamps_64) > 0):
        raise ValueError("Timestamps are not strictly monotonically increasing (duplicates or out of order detected).")
        
    return values_64, timestamps_64
