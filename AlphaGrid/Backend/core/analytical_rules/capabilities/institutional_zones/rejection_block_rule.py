from Backend.core.engine.evidence_quality import EvidenceQualityMetadata
import uuid
from typing import Optional

from Backend.core.analytical_rules.dto.liquidity.price_observation import PriceObservationDTO
from Backend.core.analytical_rules.dto.regions.region_events import RegionDetectedEventDTO
from Backend.core.analytical_rules.dto.regions.region_identity import RegionIdentityDTO, RegionType
from Backend.core.analytical_rules.dto.regions.region_geometry import RegionBoundsDTO, RegionGeometryDTO
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus

class RejectionBlockDetectionRule:
    """
    Detects a Rejection Block from a specific PriceObservation at an extreme (e.g. Swing High/Low).
    Emits a RegionDetectedEventDTO bounded by the extreme wick.
    """
    
    def evaluate(self, observation: PriceObservationDTO, structure_event_id: str, is_swing_high: bool) -> Optional[RegionDetectedEventDTO]:
        body_upper = max(observation.open, observation.close)
        body_lower = min(observation.open, observation.close)
        
        if is_swing_high:
            # Rejection block is the upper wick
            bounds = RegionBoundsDTO(upper_bound=observation.high, lower_bound=body_upper)
        else:
            # Rejection block is the lower wick
            bounds = RegionBoundsDTO(upper_bound=body_lower, lower_bound=observation.low)
            
        geom = RegionGeometryDTO(
            bounds=bounds,
            width=1.0,
            area=bounds.height * 1.0,
            geometry_fingerprint=f"REJ-{observation.observation_id}"
        )
        
        event_id = f"REJ-DETECTED-{uuid.uuid4()}"
        region_id = f"REGION-REJ-{uuid.uuid4()}"
        
        identity = RegionIdentityDTO(
            region_id=region_id,
            region_type=RegionType.REJECTION_BLOCK,
            anchor_ids=[observation.observation_id, structure_event_id],
            graph_namespace="regions/rejection_block",
            policy_checksum="none",
            geometry_fingerprint=geom.geometry_fingerprint
        )
        
        return RegionDetectedEventDTO(
            identity=EvidenceIdentityDTO(
                evidence_id=event_id,
                evidence_type="RegionDetectedEvent",
                capability_id="CAP-REJ-DETECTION",
                ontology_id="ONT-REGION-DETECTED-EVENT"
            ),
            metadata=EvidenceMetadataDTO("1.0", "1.0", "none", "none", "1.0", "1.0", event_id, {}),
            provenance=EvidenceProvenanceDTO(
                producer_rule="RejectionBlockDetectionRule",
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
            bounds=bounds,
            width=1.0,
            anchor_observation_ids=[observation.observation_id]
        )
