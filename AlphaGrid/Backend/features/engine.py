"""Feature Engine for executing the Feature DAG."""

import logging
from typing import Any, Dict, List
from Shared.models.market import MarketSnapshot
from .registry import FeatureRegistry
from .cache import FeatureCache
from .base import AbstractFeature

logger = logging.getLogger(__name__)


class FeatureEngine:
    """
    Orchestrates the evaluation of all registered features per market event.
    Ensures correct execution order (DAG), caches dependencies, and handles warm-up.
    """

    def __init__(self, registry: FeatureRegistry) -> None:
        self._registry = registry
        self._cache = FeatureCache()
        
        # Instantiate features in topological order
        self._feature_instances: List[AbstractFeature] = [
            cls() for cls in self._registry.build_dag()
        ]
        
        # Track warm-up counts per feature
        self._warmup_counts: Dict[str, int] = {
            f.get_name(): 0 for f in self._feature_instances
        }

    def process(self, snapshot: MarketSnapshot) -> Dict[str, Any]:
        """
        Processes a single market snapshot and computes all features.
        
        Args:
            snapshot: The incoming market event.
            
        Returns:
            Dictionary mapping feature names to their computed values.
        """
        self._cache.clear()
        
        for feature in self._feature_instances:
            name = feature.get_name()
            
            # Increment warm-up counter
            self._warmup_counts[name] += 1
            
            # Check if warmed up
            if self._warmup_counts[name] <= feature.warmup_period():
                # Feature is still warming up, update its internal state but return None
                try:
                    feature.compute(snapshot, self._cache.get_all())
                except Exception:
                    pass # Ignore errors during warmup, features should handle insufficient data gracefully
                self._cache.set(name, None)
                continue
                
            # Compute feature
            try:
                value = feature.compute(snapshot, self._cache.get_all())
                self._cache.set(name, value)
            except Exception as e:
                logger.error(f"Feature computation failed for '{name}': {e}")
                # Phase 8 Rule: Feature computation failure -> fail the experiment.
                raise RuntimeError(f"Feature computation failed for '{name}'") from e
                
        return self._cache.get_all()
