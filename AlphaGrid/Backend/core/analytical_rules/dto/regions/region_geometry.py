from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass(frozen=True)
class RegionBoundsDTO:
    upper_bound: float
    lower_bound: float

    @property
    def center_price(self) -> float:
        return (self.upper_bound + self.lower_bound) / 2.0
        
    @property
    def height(self) -> float:
        return self.upper_bound - self.lower_bound

@dataclass(frozen=True)
class RegionGeometryDTO:
    """
    Immutable representation of a bounded geometric region.
    """
    bounds: RegionBoundsDTO
    width: float # Time dimension approximation
    area: float
    geometry_fingerprint: str
    
    @property
    def reference_points(self) -> Dict[str, float]:
        """
        Dynamically calculates standard geometric references based on bounds.
        """
        return {
            "UPPER_BOUND": self.bounds.upper_bound,
            "LOWER_BOUND": self.bounds.lower_bound,
            "CENTER": self.bounds.center_price,
            "25_PERCENT": self.bounds.lower_bound + (self.bounds.height * 0.25),
            "75_PERCENT": self.bounds.lower_bound + (self.bounds.height * 0.75)
        }

@dataclass(frozen=True)
class OrderBlockGeometryDTO(RegionGeometryDTO):
    """
    Rich geometric representation of an Order Block.
    Provides the full raw candle breakdown so that Platform 10 remains objective.
    Platform 11 methodology plugins will decide which bound constitutes "the order block".
    """
    whole_candle_bounds: RegionBoundsDTO
    body_bounds: RegionBoundsDTO
    upper_wick_bounds: RegionBoundsDTO
    lower_wick_bounds: RegionBoundsDTO
    
    @property
    def reference_points(self) -> Dict[str, float]:
        """
        Expands standard reference points with OB-specific references.
        """
        refs = super().reference_points
        refs.update({
            "HIGH": self.whole_candle_bounds.upper_bound,
            "LOW": self.whole_candle_bounds.lower_bound,
            "OPEN": self.body_bounds.upper_bound if self.body_bounds else None, # Simplified, we don't know dir here
            "CLOSE": self.body_bounds.lower_bound if self.body_bounds else None,
            "MIDPOINT": self.whole_candle_bounds.center_price,
            "BODY_MIDPOINT": self.body_bounds.center_price if self.body_bounds else None
        })
        return {k: v for k, v in refs.items() if v is not None}
