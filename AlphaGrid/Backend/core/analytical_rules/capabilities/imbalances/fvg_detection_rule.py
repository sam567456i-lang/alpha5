from Backend.core.engine.evidence_quality import EvidenceQualityMetadata
from typing import List, Optional
import uuid

from Backend.core.analytical_rules.dto.liquidity.price_observation import PriceObservationDTO
from Backend.core.analytical_rules.dto.regions.region_events import RegionDetectedEventDTO
from Backend.core.analytical_rules.dto.regions.region_identity import RegionIdentityDTO, RegionType
from Backend.core.analytical_rules.dto.regions.region_geometry import RegionBoundsDTO
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus

class FVGDetectionRule:
    """
    Pure geometric detector for Fair Value Gaps.
    Analyzes a 3-candle rolling window and emits RegionDetectedEventDTO if a gap exists.
    Direction (Bullish/Bearish) is NOT classified at this layer.
    """
    
    def evaluate(self, observations: List[PriceObservationDTO]) -> Optional[RegionDetectedEventDTO]:
        if len(observations) != 3:
            return None
            
        obs1, obs2, obs3 = observations
        
        lower_bound = None
        upper_bound = None
        
        # Check gap where obs1 is below obs3
        if obs1.high < obs3.low:
            lower_bound = obs1.high
            upper_bound = obs3.low
        # Check gap where obs1 is above obs3
        elif obs1.low > obs3.high:
            lower_bound = obs3.high
            upper_bound = obs1.low
            
        if lower_bound is None or upper_bound is None:
            return None
            
        event_id = f"IMBALANCE-DETECTED-{uuid.uuid4()}"
        region_id = f"REGION-{uuid.uuid4()}"
        
        region_identity = RegionIdentityDTO(
            region_id=region_id,
            region_type=RegionType.FVG,
            anchor_ids=[obs1.observation_id, obs2.observation_id, obs3.observation_id],
            graph_namespace="regions/fvg",
            policy_checksum="none",
            geometry_fingerprint=f"{lower_bound}-{upper_bound}"
        )
        
        bounds = RegionBoundsDTO(upper_bound=upper_bound, lower_bound=lower_bound)
        
        return RegionDetectedEventDTO(
            identity=EvidenceIdentityDTO(
                evidence_id=event_id,
                evidence_type="RegionDetectedEvent",
                capability_id="CAP-REGION-DETECTION",
                ontology_id="ONT-REGION-DETECTED-EVENT"
            ),
            metadata=EvidenceMetadataDTO(
                schema_version="1.0.0",
                rule_version="1.0.0",
                rule_checksum="none",
                registry_checksum="none",
                sdk_version="1.0.0",
                planner_version="1.0.0",
                fingerprint=event_id,
                custom_tags={}
            ),
            provenance=EvidenceProvenanceDTO(
                producer_rule="FVGDetectionRule",
                execution_mode="Standard",
                execution_timestamp=obs3.timestamp,
                source_evidence_ids=[obs1.observation_id, obs2.observation_id, obs3.observation_id],
                market_dataset_id="MKT-123"
            ),
            classification=EvidenceClassification.COMPOSITE,
            interpretation_level=InterpretationLevel.OBJECTIVE,
            validity_status=ValidityStatus.ACTIVE,
            evidence_data={},
            quality=EvidenceQualityMetadata(confidence=1.0, coverage=1.0, freshness=0.0, latency=0.0, source_quality=1.0, sample_size=1, stability=1.0),
            superseded_by=None,
            region_identity=region_identity,
            bounds=bounds,
            width=3.0,
            anchor_observation_ids=[obs1.observation_id, obs2.observation_id, obs3.observation_id]
        )
