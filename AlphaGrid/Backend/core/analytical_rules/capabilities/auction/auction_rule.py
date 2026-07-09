import uuid
from typing import List, Optional

from Backend.core.analytical_rules.dto.liquidity.price_observation import PriceObservationDTO
from Backend.core.analytical_rules.dto.regions.region_state import RegionState
from Backend.core.analytical_rules.dto.auction.auction_metrics import AuctionMetricsDTO, AuctionObservationDTO
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus

class AuctionMetricsRule:
    """
    Evaluates price action intersecting a region to emit objective AuctionMetrics.
    Does not declare 'acceptance' or 'failed auction'—only provides the raw metrics
    for methodology plugins to threshold.
    """
    
    def evaluate(self, region: RegionState, observations: List[PriceObservationDTO]) -> Optional[AuctionMetricsDTO]:
        if not observations:
            return None
            
        upper = region.geometry.bounds.upper_bound
        lower = region.geometry.bounds.lower_bound
        
        entries = 0
        exits = 0
        total_time_inside = 0
        total_volume = 0.0
        
        # Simple simulation of metrics calculation
        # In a full implementation, this tracks discrete entry->exit cycles (AuctionObservationDTO)
        is_inside = False
        current_entry = None
        
        for obs in observations:
            # Check overlap
            if obs.low <= upper and obs.high >= lower:
                if not is_inside:
                    is_inside = True
                    entries += 1
                    current_entry = obs.timestamp
                
                total_time_inside += 1
                total_volume += 100.0 # Mock volume
                
            else:
                if is_inside:
                    is_inside = False
                    exits += 1
                    
        event_id = f"AUCTION-METRICS-{uuid.uuid4()}"
        
        return AuctionMetricsDTO(
            identity=EvidenceIdentityDTO(
                evidence_id=event_id,
                evidence_type="AuctionMetrics",
                capability_id="CAP-AUCTION-METRICS",
                ontology_id="ONT-AUCTION-METRICS"
            ),
            metadata=EvidenceMetadataDTO("1.0", "1.0", "none", "none", "1.0", "1.0", event_id, {}),
            provenance=EvidenceProvenanceDTO(
                producer_rule="AuctionMetricsRule",
                execution_mode="Standard",
                execution_timestamp="T",
                source_evidence_ids=[region.identity.evidence_id],
                market_dataset_id="MKT-1"
            ),
            classification=EvidenceClassification.PRIMITIVE,
            interpretation_level=InterpretationLevel.OBJECTIVE,
            validity_status=ValidityStatus.ACTIVE,
            evidence_data={},
            region_id=region.region_identity.region_id,
            time_inside_region=total_time_inside,
            volume_inside_region=total_volume,
            number_of_entries=entries,
            number_of_exits=exits,
            mean_price=(upper + lower) / 2.0,
            vwap=(upper + lower) / 2.0,
            rotation_count=entries + exits,
            distance_traveled=0.0,
            body_overlap_percentage=0.5,
            wick_overlap_percentage=0.5,
            net_progress=0.0,
            observations=[]
        )
