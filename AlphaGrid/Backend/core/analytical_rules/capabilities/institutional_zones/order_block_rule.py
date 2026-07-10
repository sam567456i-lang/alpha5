from Backend.core.engine.evidence_quality import EvidenceQualityMetadata
import uuid
from typing import Optional

from Backend.core.analytical_rules.dto.liquidity.price_observation import PriceObservationDTO
from Backend.core.analytical_rules.dto.regions.region_events import RegionDetectedEventDTO
from Backend.core.analytical_rules.dto.regions.region_identity import RegionIdentityDTO, RegionType
from Backend.core.analytical_rules.dto.regions.region_geometry import RegionBoundsDTO, OrderBlockGeometryDTO
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus

class OrderBlockDetectionRule:
    """
    Detects an Order Block from a specific PriceObservation (e.g. the candle that caused a BOS).
    Emits an objective OrderBlockGeometryDTO so that methodologies can decide which part of 
    the block to use.
    """
    
    def evaluate(self, observation: PriceObservationDTO, structure_event_id: str) -> Optional[RegionDetectedEventDTO]:
        # For an objective Order Block, we parse the single observation into rich geometry
        
        whole_candle = RegionBoundsDTO(upper_bound=observation.high, lower_bound=observation.low)
        
        # Determine body bounds based on open and close
        body_upper = max(observation.open, observation.close)
        body_lower = min(observation.open, observation.close)
        body = RegionBoundsDTO(upper_bound=body_upper, lower_bound=body_lower)
        
        upper_wick = RegionBoundsDTO(upper_bound=observation.high, lower_bound=body_upper)
        lower_wick = RegionBoundsDTO(upper_bound=body_lower, lower_bound=observation.low)
        
        geom = OrderBlockGeometryDTO(
            bounds=whole_candle, # Default overall bounds
            width=1.0, # Single observation
            area=whole_candle.height * 1.0,
            geometry_fingerprint=f"OB-{observation.observation_id}",
            whole_candle_bounds=whole_candle,
            body_bounds=body,
            upper_wick_bounds=upper_wick,
            lower_wick_bounds=lower_wick
        )
        
        event_id = f"OB-DETECTED-{uuid.uuid4()}"
        region_id = f"REGION-OB-{uuid.uuid4()}"
        
        identity = RegionIdentityDTO(
            region_id=region_id,
            region_type=RegionType.ORDER_BLOCK,
            anchor_ids=[observation.observation_id, structure_event_id],
            graph_namespace="regions/order_block",
            policy_checksum="none",
            geometry_fingerprint=geom.geometry_fingerprint
        )
        
        return RegionDetectedEventDTO(
            identity=EvidenceIdentityDTO(
                evidence_id=event_id,
                evidence_type="RegionDetectedEvent",
                capability_id="CAP-OB-DETECTION",
                ontology_id="ONT-REGION-DETECTED-EVENT"
            ),
            metadata=EvidenceMetadataDTO("1.0", "1.0", "none", "none", "1.0", "1.0", event_id, {}),
            provenance=EvidenceProvenanceDTO(
                producer_rule="OrderBlockDetectionRule",
                execution_mode="Standard",
                execution_timestamp=observation.timestamp,
                source_evidence_ids=[observation.observation_id, structure_event_id],
                market_dataset_id="MKT-1"
            ),
            classification=EvidenceClassification.PRIMITIVE,
            interpretation_level=InterpretationLevel.OBJECTIVE,
            validity_status=ValidityStatus.ACTIVE,
            evidence_data={},
            quality=EvidenceQualityMetadata(confidence=1.0, coverage=1.0, freshness=0.0, latency=0.0, source_quality=1.0, sample_size=1, stability=1.0),
            superseded_by=None,
            region_identity=identity,
            bounds=whole_candle,
            width=1.0,
            anchor_observation_ids=[observation.observation_id]
        )
