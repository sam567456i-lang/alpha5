"""Relative Volume (RVOL) Feature Generator."""

from typing import Any, Dict, List, Optional
from Shared.models.market import MarketSnapshot
from Backend.features.base import AbstractFeature

class RelativeVolumeFeature(AbstractFeature):
    """
    Calculates Relative Volume (RVOL) over a specified period.
    RVOL = Current Volume / SMA(Volume, period)
    """
    
    def __init__(self) -> None:
        self.period = 14
        self._volume_history: List[int] = []

    @classmethod
    def get_name(cls) -> str:
        return "RVOL_14"

    @classmethod
    def get_version(cls) -> str:
        return "v1"

    @classmethod
    def get_dependencies(cls) -> List[str]:
        return []

    @classmethod
    def warmup_period(cls) -> int:
        return 14

    def compute(self, snapshot: MarketSnapshot, dependency_values: Dict[str, Any]) -> Optional[Dict[str, float]]:
        self._volume_history.append(snapshot.volume)
        
        if len(self._volume_history) > self.period:
            self._volume_history.pop(0)
            
        if len(self._volume_history) < self.period:
            return {
                "rvol": 1.0,
                "sma_volume": float(snapshot.volume),
                "current_volume": float(snapshot.volume)
            }
            
        sma_volume = sum(self._volume_history) / self.period
        rvol = snapshot.volume / sma_volume if sma_volume > 0 else 1.0
        
        return {
            "rvol": float(rvol),
            "sma_volume": float(sma_volume),
            "current_volume": float(snapshot.volume)
        }
