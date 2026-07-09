import uuid
from typing import Optional

from Backend.core.analytical_rules.dto.delivery.delivery_metrics import DeliveryMetricsDTO, PriceTraversalDTO
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus

class DeliveryMetricsRule:
    """
    Evaluates a PriceTraversalDTO to emit objective momentum properties.
    """
    
    def evaluate(self, traversal: PriceTraversalDTO) -> Optional[DeliveryMetricsDTO]:
        if not traversal.observations or len(traversal.observations) < 2:
            return None
            
        candles = traversal.observations
        candle_count = len(candles)
        
        # Calculate raw distance
        start_price = candles[0].open
        end_price = candles[-1].close
        distance = abs(end_price - start_price)
        
        # Time (assuming each observation is 1 unit for now, or parsing timestamps)
        time_elapsed = candle_count
        
        velocity = distance / time_elapsed if time_elapsed > 0 else 0.0
        
        total_body = sum(abs(c.close - c.open) for c in candles)
        total_range = sum(c.high - c.low for c in candles)
        
        body_ratio = total_body / total_range if total_range > 0 else 0.0
        average_body = total_body / candle_count
        maximum_body = max(abs(c.close - c.open) for c in candles)
        
        # Calculate gap and overlap
        # Overlap is the intersecting price range between adjacent candles
        total_overlap = 0.0
        min_overlap = float('inf')
        for i in range(1, candle_count):
            prev = candles[i-1]
            curr = candles[i]
            
            overlap_high = min(prev.high, curr.high)
            overlap_low = max(prev.low, curr.low)
            overlap = max(0.0, overlap_high - overlap_low)
            total_overlap += overlap
            if overlap < min_overlap:
                min_overlap = overlap
                
        if min_overlap == float('inf'):
            min_overlap = 0.0
            
        overlap_ratio = total_overlap / total_range if total_range > 0 else 0.0
        
        event_id = f"DELIVERY-METRICS-{uuid.uuid4()}"
        
        return DeliveryMetricsDTO(
            identity=EvidenceIdentityDTO(
                evidence_id=event_id,
                evidence_type="DeliveryMetrics",
                capability_id="CAP-DELIVERY-METRICS",
                ontology_id="ONT-DELIVERY-METRICS"
            ),
            metadata=EvidenceMetadataDTO("1.0", "1.0", "none", "none", "1.0", "1.0", event_id, {}),
            provenance=EvidenceProvenanceDTO(
                producer_rule="DeliveryMetricsRule",
                execution_mode="Standard",
                execution_timestamp="T",
                source_evidence_ids=[traversal.start_point_id, traversal.end_point_id],
                market_dataset_id="MKT-1"
            ),
            classification=EvidenceClassification.PRIMITIVE,
            interpretation_level=InterpretationLevel.OBJECTIVE,
            validity_status=ValidityStatus.ACTIVE,
            evidence_data={},
            traversal_id=f"TRAVERSAL-{traversal.start_point_id}-{traversal.end_point_id}",
            velocity=velocity,
            acceleration=0.0, # Derivative of velocity, hard to mock without full context
            body_ratio=body_ratio,
            wick_ratio=1.0 - body_ratio,
            gap_ratio=0.0, # Could be calculated from FVG detection
            overlap_ratio=overlap_ratio,
            atr_ratio=0.0, # Requires ATR provider
            distance=distance,
            time_elapsed=time_elapsed,
            candle_count=candle_count,
            average_body=average_body,
            maximum_body=maximum_body,
            minimum_overlap=min_overlap,
            impulse_score=velocity * body_ratio
        )
