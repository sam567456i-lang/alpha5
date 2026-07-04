from typing import Protocol
import numpy as np

class ExecutionBackend(Protocol):
    def ema_loop(self, values: np.ndarray, out: np.ndarray, valid_mask: np.ndarray, start_idx: int, alpha: float) -> None:
        ...

# Global registry or resolution mechanism
_backend = None

def get_backend() -> ExecutionBackend:
    global _backend
    if _backend is None:
        try:
            from Backend.math.runtime.numba_backend import NumbaBackend
            _backend = NumbaBackend()
        except ImportError:
            from Backend.math.runtime.numpy_backend import NumpyBackend
            _backend = NumpyBackend()
    return _backend
