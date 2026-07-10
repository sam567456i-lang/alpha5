from Backend.core.engine.evidence_quality import EvidenceQualityMetadata
import uuid
from enum import Enum
from typing import Optional

from Backend.core.analytical_rules.dto.liquidity.pool_state import PoolState
from Backend.core.analytical_rules.dto.range.range_state import RangeState
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus
from Backend.core.analytical_rules.dto.evidence_dto import EvidenceDTO
from dataclasses import dataclass

class RangeLiquidityLocation(Enum):
    INSIDE = "INSIDE"
    BOUNDARY = "BOUNDARY"
    OUTSIDE = "OUTSIDE"

@dataclass(frozen=True)
class RangeLiquidityRelationshipDTO(EvidenceDTO):
    """
    Graph edge establishing the topological relationship between a liquidity pool and a range.
    """
    range_id: str
    pool_id: str
    location: RangeLiquidityLocation

class RangeLiquidityRelationshipRule:
    """
    Classifies a LiquidityPool against a RangeState to establish structural topology.
    IRL and ERL are derived purely from these objective locations.
    """
    
    def evaluate(self, range_state: RangeState, pool_state: PoolState, tolerance: float = 0.01) -> Optional[RangeLiquidityRelationshipDTO]:
        pool_price = pool_state.center_price
        
        # Check if pool is on the boundary
        is_upper_boundary = abs(pool_price - range_state.upper_bound) <= tolerance
        is_lower_boundary = abs(pool_price - range_state.lower_bound) <= tolerance
        
        if is_upper_boundary or is_lower_boundary:
            location = RangeLiquidityLocation.BOUNDARY
        elif pool_price < range_state.upper_bound and pool_price > range_state.lower_bound:
            location = RangeLiquidityLocation.INSIDE
        else:
            location = RangeLiquidityLocation.OUTSIDE
            
        event_id = f"RANGE-LIQ-REL-{uuid.uuid4()}"
        
        return RangeLiquidityRelationshipDTO(
            identity=EvidenceIdentityDTO(
                evidence_id=event_id,
                evidence_type="RangeLiquidityRelationship",
                capability_id="CAP-RANGE-LIQUIDITY",
                ontology_id="ONT-RANGE-RELATIONSHIP"
            ),
            metadata=EvidenceMetadataDTO("1.0", "1.0", "none", "none", "1.0", "1.0", event_id, {}),
            provenance=EvidenceProvenanceDTO(
                producer_rule="RangeLiquidityRelationshipRule",
                execution_mode="Standard",
                execution_timestamp="T",
                source_evidence_ids=[range_state.range_id, pool_state.pool_identity.pool_id],
                market_dataset_id="MKT-1"
            ),
            classification=EvidenceClassification.DERIVED,
            interpretation_level=InterpretationLevel.OBJECTIVE,
            validity_status=ValidityStatus.ACTIVE,
            evidence_data={},
            quality=EvidenceQualityMetadata(confidence=1.0, coverage=1.0, freshness=0.0, latency=0.0, source_quality=1.0, sample_size=1, stability=1.0),
            superseded_by=None,
            range_id=range_state.range_id,
            pool_id=pool_state.pool_identity.pool_id,
            location=location
        )
