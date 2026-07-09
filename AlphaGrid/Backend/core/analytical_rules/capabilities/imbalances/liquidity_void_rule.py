import uuid
from typing import Optional, List

from Backend.core.analytical_rules.dto.regions.region_events import RegionDetectedEventDTO
from Backend.core.analytical_rules.dto.regions.region_identity import RegionIdentityDTO, RegionType
from Backend.core.analytical_rules.dto.regions.region_geometry import RegionBoundsDTO
from Backend.core.analytical_rules.dto.regions.region_state import RegionState
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus

class LiquidityVoidRule:
    """
    Derived rule that creates a macro Liquidity Void region 
    by consuming multiple adjacent/contiguous FVG RegionStates.
    """
    
    def evaluate(self, fvgs: List[RegionState]) -> Optional[RegionDetectedEventDTO]:
        if not fvgs or len(fvgs) < 2:
            return None
            
        for fvg in fvgs:
            if fvg.region_identity.region_type != RegionType.FVG:
                return None
                
        # To form a void, we aggregate the geometry of the contiguous gaps
        upper_bound = max([fvg.geometry.bounds.upper_bound for fvg in fvgs])
        lower_bound = min([fvg.geometry.bounds.lower_bound for fvg in fvgs])
        
        event_id = f"VOID-DETECTED-{uuid.uuid4()}"
        region_id = f"REGION-VOID-{uuid.uuid4()}"
        source_ids = [fvg.identity.evidence_id for fvg in fvgs]
        
        region_identity = RegionIdentityDTO(
            region_id=region_id,
            region_type=RegionType.LIQUIDITY_VOID,
            anchor_ids=source_ids,
            graph_namespace="regions/void",
            policy_checksum="none",
            geometry_fingerprint=f"{lower_bound}-{upper_bound}"
        )
        
        bounds = RegionBoundsDTO(upper_bound=upper_bound, lower_bound=lower_bound)
        
        return RegionDetectedEventDTO(
            identity=EvidenceIdentityDTO(
                evidence_id=event_id,
                evidence_type="RegionDetectedEvent",
                capability_id="CAP-VOID-DETECTION",
                ontology_id="ONT-REGION-DETECTED-EVENT"
            ),
            metadata=EvidenceMetadataDTO("1.0", "1.0", "none", "none", "1.0", "1.0", event_id, {}),
            provenance=EvidenceProvenanceDTO(
                producer_rule="LiquidityVoidRule",
                execution_mode="Standard",
                execution_timestamp="T",
                source_evidence_ids=source_ids,
                market_dataset_id="MKT-1"
            ),
            classification=EvidenceClassification.DERIVED,
            interpretation_level=InterpretationLevel.OBJECTIVE,
            validity_status=ValidityStatus.ACTIVE,
            evidence_data={},
            region_identity=region_identity,
            bounds=bounds,
            width=sum([fvg.geometry.width for fvg in fvgs]), 
            anchor_observation_ids=[]
        )
