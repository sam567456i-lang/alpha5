from typing import Dict, List, Any
from datetime import datetime
from Backend.core.evidence_dtos.liquidity import ReferenceLevel, ReferenceType
from Backend.core.engines.lifecycle import BaseObjectLifecycleEngine
from Backend.core.analytical_rules.liquidity_rules import ReferenceLevelExtractionRule
from Backend.core.evidence_dtos.base import LifecycleState

class ReferenceLevelEngine:
    """
    Orchestrates the extraction, caching, and lifecycle management of Reference Levels.
    """
    def __init__(self, lifecycle_engine: BaseObjectLifecycleEngine):
        self.lifecycle_engine = lifecycle_engine
        self.extraction_rule = ReferenceLevelExtractionRule()
        
        # Performance Cache: keys by ReferenceType and interval_identifier
        # e.g., (ReferenceType.PREVIOUS_DAY_HIGH, '2026-07-08') -> ReferenceLevel Object
        self._cache: Dict[tuple, ReferenceLevel] = {}

    def _get_cache_key(self, level: ReferenceLevel) -> tuple:
        return (level.reference_type, level.interval_identifier)

    def process_tick(self, current_timestamp: datetime, historical_data: Dict[str, Any]) -> List[ReferenceLevel]:
        """
        Invoked on every new tick/bar.
        """
        active_levels = []
        
        # 1. Extract raw levels from data
        extracted_levels = self.extraction_rule.extract(current_timestamp, historical_data)
        
        # 2. Check Cache
        for level in extracted_levels:
            cache_key = self._get_cache_key(level)
            if cache_key in self._cache:
                # Use the cached immutable identity/object
                cached_obj = self._cache[cache_key]
                
                # Optionally run lifecycle transition if it's new for this tick
                if cached_obj.state == LifecycleState.CANDIDATE:
                    from Backend.core.engines.lifecycle import LifecycleEvent
                    self.lifecycle_engine.process_event(cached_obj, LifecycleEvent.VALIDATE_REQUESTED)
                    self.lifecycle_engine.process_event(cached_obj, LifecycleEvent.CONFIRM_REQUESTED)
                    self.lifecycle_engine.process_event(cached_obj, LifecycleEvent.ACTIVATE_REQUESTED)
                
                active_levels.append(cached_obj)
            else:
                # Brand new reference level discovered
                from Backend.core.engines.lifecycle import LifecycleEvent
                self.lifecycle_engine.process_event(level, LifecycleEvent.VALIDATE_REQUESTED)
                self.lifecycle_engine.process_event(level, LifecycleEvent.CONFIRM_REQUESTED)
                self.lifecycle_engine.process_event(level, LifecycleEvent.ACTIVATE_REQUESTED)
                
                self._cache[cache_key] = level
                active_levels.append(level)
                
        return active_levels
