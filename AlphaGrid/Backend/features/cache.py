"""Feature Cache for Dependency Injection."""

import threading
from typing import Any, Dict


class FeatureCache:
    """
    Holds the computed feature values for a single market event.
    Passed to each feature so it can read its dependencies.
    """

    def __init__(self) -> None:
        self._cache: Dict[str, Any] = {}
        self._lock = threading.Lock()

    def set(self, feature_name: str, value: Any) -> None:
        """Stores the computed value of a feature."""
        with self._lock:
            self._cache[feature_name] = value

    def get(self, feature_name: str) -> Any:
        """Retrieves a computed feature value."""
        with self._lock:
            return self._cache.get(feature_name)

    def get_all(self) -> Dict[str, Any]:
        """Returns the full dictionary of computed values."""
        with self._lock:
            return self._cache.copy()

    def clear(self) -> None:
        """Clears the cache (should be called before processing the next event)."""
        with self._lock:
            self._cache.clear()
