from dataclasses import dataclass
from typing import List

from Backend.core.analytical_rules.dto.evidence_dto import EvidenceDTO
from Backend.core.analytical_rules.dto.liquidity.price_observation import PriceObservationDTO

@dataclass(frozen=True)
class PriceTraversalDTO:
    """
    Represents the path price took between two structural or regional events.
    Stateless property of a path, not a persisting region or structure.
    """
    start_point_id: str
    end_point_id: str
    observations: List[PriceObservationDTO]
    
@dataclass(frozen=True)
class DeliveryMetricsDTO(EvidenceDTO):
    """
    Objective momentum properties derived from a PriceTraversal.
    Does not declare 'Displacement' or 'Efficient Delivery'.
    Provides the raw metrics for plugins to threshold.
    """
    traversal_id: str
    velocity: float # Price units per observation
    acceleration: float 
    body_ratio: float # Average (body / total candle size)
    wick_ratio: float
    gap_ratio: float
    overlap_ratio: float # How much adjacent candles overlap
    atr_ratio: float # (traversal height / average ATR)
    distance: float
    time_elapsed: int
    candle_count: int
    average_body: float
    maximum_body: float
    minimum_overlap: float
    impulse_score: float # Synthetic objective score based on continuous progression
