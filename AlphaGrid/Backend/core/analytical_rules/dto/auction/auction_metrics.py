from dataclasses import dataclass
from typing import List

from Backend.core.analytical_rules.dto.evidence_dto import EvidenceDTO
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO

@dataclass(frozen=True)
class AuctionObservationDTO:
    """
    Represents a single entry-to-exit cycle within a region boundary.
    """
    entry_timestamp: str
    exit_timestamp: str
    time_inside: int
    volume_inside: float
    max_excursion: float
    min_excursion: float

@dataclass(frozen=True)
class AuctionMetricsDTO(EvidenceDTO):
    """
    Objective measurements of price action interacting with a specific Region.
    These metrics are consumed by methodology plugins (e.g., Platform 11) to decide 
    if an auction was accepted, rejected, or failed.
    """
    region_id: str
    
    # Raw objective metrics
    time_inside_region: int
    volume_inside_region: float
    number_of_entries: int
    number_of_exits: int
    mean_price: float
    vwap: float
    rotation_count: int
    distance_traveled: float
    body_overlap_percentage: float
    wick_overlap_percentage: float
    net_progress: float
    
    observations: List[AuctionObservationDTO]
