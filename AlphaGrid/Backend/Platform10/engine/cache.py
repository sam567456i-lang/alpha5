import hashlib
import json
from typing import Dict, Optional, Tuple
from Backend.Platform10.contracts.dtos import MarketStateDTO, MethodologyResultDTO, ExecutionTraceDTO

class ExecutionCache:
    """Platform 10 Cache - Caches outputs based on immutable inputs."""
    
    def __init__(self):
        self._cache: Dict[str, Tuple[MethodologyResultDTO, ExecutionTraceDTO]] = {}
        
    def _hash_state(self, plugin_id: str, market_state: MarketStateDTO) -> str:
        """
        Creates a deterministic hash of the required state for a specific plugin.
        For robust caching, this hashes the features and timestamp.
        """
        # A true prod system would sort and serialize safely.
        state_repr = json.dumps({
            "features": market_state.features.features,
            "timestamp": market_state.context.timestamp,
            "symbol": market_state.symbol,
            "timeframe": market_state.timeframe
        }, sort_keys=True)
        
        return hashlib.sha256(f"{plugin_id}_{state_repr}".encode('utf-8')).hexdigest()
        
    def get(self, plugin_id: str, market_state: MarketStateDTO) -> Optional[Tuple[MethodologyResultDTO, ExecutionTraceDTO]]:
        state_hash = self._hash_state(plugin_id, market_state)
        return self._cache.get(state_hash)
        
    def set(self, plugin_id: str, market_state: MarketStateDTO, result: MethodologyResultDTO, trace: ExecutionTraceDTO):
        state_hash = self._hash_state(plugin_id, market_state)
        self._cache[state_hash] = (result, trace)
