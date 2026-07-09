import uuid
from typing import Optional, List

from Backend.core.analytical_rules.dto.regions.region_context import RegionInteractionContextDTO
from Backend.core.analytical_rules.dto.regions.region_events import RegionReferenceInteractionEventDTO, RegionReferenceType
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus

class RegionInteractionRule:
    """
    Stateless rule that evaluates if a PriceObservation interacts with specific
    mathematical references inside a Region. Emits RegionReferenceInteractionEventDTO.
    """
    
    def evaluate(self, context: RegionInteractionContextDTO) -> List[RegionReferenceInteractionEventDTO]:
        events = []
        obs = context.observation
        geom = context.region_geometry
        refs = geom.reference_points
        
        # Determine if the observation interacts with the target references
        # An interaction occurs if the observation's high/low range crosses or touches the reference price
        
        for target_ref in context.target_references:
            # Full Fill and Partial Fill are special logic, handled here generically or in lifecycle?
            # Actually, FULL_FILL and PARTIAL_FILL can be determined if the observation crosses the bound.
            
            # Let's do simple crossing check for standard references
            if target_ref.name in refs:
                ref_price = refs[target_ref.name]
                if obs.low <= ref_price <= obs.high:
                    events.append(self._create_event(context, target_ref, ref_price))
                    
            # Handle special cases like FULL_FILL where price completely crosses the region
            if target_ref == RegionReferenceType.FILL_FULL:
                # If it's a gap up (lower bound is high, upper bound is low), a full fill means price went below lower bound.
                # Since geometry doesn't have direction, a full fill means price has touched/crossed the opposite bound.
                # We can approximate this by saying if the price observation spans both upper and lower bounds.
                # Actually, "fill" depends on the region. A more robust way is crossing the bounds.
                # For now, let's just say a full fill is crossing the lower bound if coming from above, etc.
                # We'll simplify: if price covers the entire region's height.
                if obs.low <= geom.bounds.lower_bound and obs.high >= geom.bounds.upper_bound:
                    events.append(self._create_event(context, RegionReferenceType.FILL_FULL, geom.bounds.center_price))
                    
        return events
        
    def _create_event(self, context: RegionInteractionContextDTO, ref_type: RegionReferenceType, price: float) -> RegionReferenceInteractionEventDTO:
        event_id = f"REGION-INTERACT-{uuid.uuid4()}"
        return RegionReferenceInteractionEventDTO(
            identity=EvidenceIdentityDTO(
                evidence_id=event_id,
                evidence_type="RegionReferenceInteractionEvent",
                capability_id="CAP-REGION-INTERACTION",
                ontology_id="ONT-REGION-INTERACT-EVENT"
            ),
            metadata=EvidenceMetadataDTO("1.0", "1.0", "none", "none", "1.0", "1.0", event_id, {}),
            provenance=EvidenceProvenanceDTO(
                producer_rule="RegionInteractionRule",
                execution_mode="Standard",
                execution_timestamp=context.observation.timestamp,
                source_evidence_ids=[context.region_identity.region_id, context.observation.observation_id],
                market_dataset_id="MKT-1"
            ),
            classification=EvidenceClassification.COMPOSITE,
            interpretation_level=InterpretationLevel.OBJECTIVE,
            validity_status=ValidityStatus.ACTIVE,
            evidence_data={},
            region_identity=context.region_identity,
            reference_type=ref_type,
            interaction_price=price,
            interaction_observation_id=context.observation.observation_id
        )
