from typing import Dict, List
from Backend.core.research.assets.registry.scenario_registry import MarketRegime

class AssetRegistry:
    """Tracks overall asset coverage across regimes to identify research blind spots."""
    
    def __init__(self):
        self._coverage_matrix: Dict[MarketRegime, int] = {regime: 0 for regime in MarketRegime}
        
    def log_asset(self, regime: MarketRegime):
        self._coverage_matrix[regime] += 1
        
    def get_coverage_gaps(self) -> List[MarketRegime]:
        """Returns regimes with zero coverage."""
        return [r for r, count in self._coverage_matrix.items() if count == 0]
