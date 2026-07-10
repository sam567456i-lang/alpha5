from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic, Any, Callable

@dataclass(frozen=True)
class NumericalPolicy:
    """Configurable tolerances for robust floating-point operations."""
    epsilon: float = 1e-9
    zero_threshold: float = 1e-12
    overflow_threshold: float = 1e308
    nan_policy: str = "PROPAGATE" # Or "DROP", "ZERO"

class MathBackend(ABC):
    """
    Abstract execution engine. Answers "How are mathematical operations executed?"
    """
    
    # --- Capability Discovery ---
    @abstractmethod
    def supports_vectorization(self) -> bool: pass
    
    @abstractmethod
    def supports_gpu(self) -> bool: pass
    
    @abstractmethod
    def supports_parallel(self) -> bool: pass
    
    @abstractmethod
    def supports_streaming(self) -> bool: pass

    # --- Abstract Mathematical Operations ---
    @abstractmethod
    def apply_numerical_policy(self, value: float, policy: NumericalPolicy) -> float:
        """Enforces zero thresholds and NaN handling."""
        pass

T = TypeVar('T')

class RollingState(Generic[T]):
    """
    A highly optimized, reusable state container designed for amortized O(1) 
    updates without triggering heap allocations during steady-state processing.
    """
    def __init__(self, window_size: int):
        self.window_size = window_size
        self._buffer = [None] * window_size
        self._index = 0
        self._count = 0
        
    def push(self, item: T) -> None:
        """O(1) push operation."""
        self._buffer[self._index] = item
        self._index = (self._index + 1) % self.window_size
        if self._count < self.window_size:
            self._count += 1
            
    def get_oldest(self) -> T:
        """Retrieves the N-periods ago item. O(1)."""
        if self._count == 0:
            return None
        if self._count < self.window_size:
            return self._buffer[0]
        return self._buffer[self._index]
        
    def get_newest(self) -> T:
        """Retrieves the most recently pushed item. O(1)."""
        if self._count == 0:
            return None
        idx = (self._index - 1) % self.window_size
        return self._buffer[idx]

    def is_full(self) -> bool:
        return self._count == self.window_size
