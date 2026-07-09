from typing import List, Dict, Any, Optional
from Backend.core.analytical_rules.dto.liquidity.liquidity_anchor import LiquidityAnchor
from Backend.core.analytical_rules.dto.liquidity.equal_primitives import EqualHighState, EqualLowState
from Backend.core.analytical_rules.dto.liquidity.equal_primitives_events import EqualHighDetectedEventDTO, EqualLowDetectedEventDTO
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.utils.identity_factory import IdentityFactory
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus

class EqualDetectorPolicy:
    def __init__(self, 
                 minimum_anchor_count: int = 2,
                 maximum_time_distance: int = 100, # e.g. periods or seconds
                 price_variance_threshold: float = 0.0,
                 anchor_types_allowed: List[str] = None,
                 confirmation_policy: str = "DEFAULT"):
        self.minimum_anchor_count = minimum_anchor_count
        self.maximum_time_distance = maximum_time_distance
        self.price_variance_threshold = price_variance_threshold
        self.anchor_types_allowed = anchor_types_allowed if anchor_types_allowed else ["NODE_STRUCTURE_SWING_HIGH", "NODE_STRUCTURE_SWING_LOW"]
        self.confirmation_policy = confirmation_policy

class EqualHighDetector:
    """
    Detects equal highs from a stream or collection of LiquidityAnchors.
    """
    def __init__(self, policy: EqualDetectorPolicy):
        self.policy = policy
        
    def detect(self, anchors: List[LiquidityAnchor]) -> List[EqualHighDetectedEventDTO]:
        events = []
        
        # Filter valid anchors
        valid_anchors = [a for a in anchors if a.origin_type in self.policy.anchor_types_allowed]
        valid_anchors.sort(key=lambda a: a.timestamp)
        
        n = len(valid_anchors)
        emitted_clusters = []
        
        for i in range(n):
            current_cluster = [valid_anchors[i]]
            
            for j in range(i + 1, n):
                candidate = valid_anchors[j]
                
                # Check if adding candidate exceeds variance threshold for the whole cluster
                prices = [a.price for a in current_cluster] + [candidate.price]
                if max(prices) - min(prices) <= self.policy.price_variance_threshold:
                    # Optional: check time distance
                    # For simplicity in Wave 2B.2A, we assume timestamps are string and just ignore time distance 
                    # unless a real datetime conversion is provided.
                    current_cluster.append(candidate)
                    
            if len(current_cluster) >= self.policy.minimum_anchor_count:
                # Check if this is a subset of an already emitted cluster
                cluster_ids = set(a.anchor_id for a in current_cluster)
                is_subset = any(cluster_ids.issubset(c) for c in emitted_clusters)
                
                if not is_subset:
                    emitted_clusters.append(cluster_ids)
                    
                    anchor_ids = [a.anchor_id for a in current_cluster]
                    avg_price = sum(a.price for a in current_cluster) / len(current_cluster)
                    variance = max(a.price for a in current_cluster) - min(a.price for a in current_cluster)
                    
                    # Generate deterministic ID
                    fingerprint = IdentityFactory.generate_geometry_fingerprint(
                        price=avg_price,
                        timestamp=current_cluster[-1].timestamp,
                        direction="HIGH",
                        timeframe="unknown",
                        symbol="unknown"
                    )
                    
                    event_id = IdentityFactory.generate_event_id("EqualHighDetectedEventDTO", fingerprint, "eqh_detector_v1")
                    
                    event = EqualHighDetectedEventDTO(
                        identity=EvidenceIdentityDTO(
                            evidence_id=event_id,
                            evidence_type="EqualHighDetectedEvent",
                            capability_id="CAP-LIQUIDITY-01",
                            ontology_id="ONT-LIQUIDITY-EQH-EVENT"
                        ),
                        metadata=EvidenceMetadataDTO(
                            schema_version="1.0.0",
                            rule_version="1.0.0",
                            rule_checksum="none",
                            registry_checksum="none",
                            sdk_version="1.0.0",
                            planner_version="1.0.0",
                            fingerprint=fingerprint,
                            custom_tags={}
                        ),
                        provenance=EvidenceProvenanceDTO(
                            producer_rule="EqualHighDetector",
                            execution_mode="Standard",
                            execution_timestamp=current_cluster[-1].timestamp,
                            source_evidence_ids=anchor_ids,
                            market_dataset_id="MKT-123"
                        ),
                        classification=EvidenceClassification.COMPOSITE,
                        interpretation_level=InterpretationLevel.OBJECTIVE,
                        validity_status=ValidityStatus.ACTIVE,
                        evidence_data={},
                        event_id=event_id,
                        event_timestamp=current_cluster[-1].timestamp,
                        trigger_rule="EqualHighDetector",
                        trigger_evidence=current_cluster[-1].anchor_id,
                        affected_state_ids=[],
                        causal_events=[],
                        severity="INFO",
                        sequence_number=1,
                        anchor_ids=anchor_ids,
                        anchor_count=len(anchor_ids),
                        average_price=avg_price,
                        price_variance=variance,
                        confidence_inputs=[]
                    )
                    events.append(event)
                    
        return events

class EqualLowDetector:
    """
    Detects equal lows from a stream or collection of LiquidityAnchors.
    """
    def __init__(self, policy: EqualDetectorPolicy):
        self.policy = policy
        
    def detect(self, anchors: List[LiquidityAnchor]) -> List[EqualLowDetectedEventDTO]:
        events = []
        
        valid_anchors = [a for a in anchors if a.origin_type in self.policy.anchor_types_allowed]
        valid_anchors.sort(key=lambda a: a.timestamp)
        
        n = len(valid_anchors)
        emitted_clusters = []
        
        for i in range(n):
            current_cluster = [valid_anchors[i]]
            
            for j in range(i + 1, n):
                candidate = valid_anchors[j]
                
                prices = [a.price for a in current_cluster] + [candidate.price]
                if max(prices) - min(prices) <= self.policy.price_variance_threshold:
                    current_cluster.append(candidate)
                    
            if len(current_cluster) >= self.policy.minimum_anchor_count:
                cluster_ids = set(a.anchor_id for a in current_cluster)
                is_subset = any(cluster_ids.issubset(c) for c in emitted_clusters)
                
                if not is_subset:
                    emitted_clusters.append(cluster_ids)
                    
                    anchor_ids = [a.anchor_id for a in current_cluster]
                    avg_price = sum(a.price for a in current_cluster) / len(current_cluster)
                    variance = max(a.price for a in current_cluster) - min(a.price for a in current_cluster)
                    
                    fingerprint = IdentityFactory.generate_geometry_fingerprint(
                        price=avg_price,
                        timestamp=current_cluster[-1].timestamp,
                        direction="LOW",
                        timeframe="unknown",
                        symbol="unknown"
                    )
                    
                    event_id = IdentityFactory.generate_event_id("EqualLowDetectedEventDTO", fingerprint, "eql_detector_v1")
                    
                    event = EqualLowDetectedEventDTO(
                        identity=EvidenceIdentityDTO(
                            evidence_id=event_id,
                            evidence_type="EqualLowDetectedEvent",
                            capability_id="CAP-LIQUIDITY-02",
                            ontology_id="ONT-LIQUIDITY-EQL-EVENT"
                        ),
                        metadata=EvidenceMetadataDTO(
                            schema_version="1.0.0",
                            rule_version="1.0.0",
                            rule_checksum="none",
                            registry_checksum="none",
                            sdk_version="1.0.0",
                            planner_version="1.0.0",
                            fingerprint=fingerprint,
                            custom_tags={}
                        ),
                        provenance=EvidenceProvenanceDTO(
                            producer_rule="EqualLowDetector",
                            execution_mode="Standard",
                            execution_timestamp=current_cluster[-1].timestamp,
                            source_evidence_ids=anchor_ids,
                            market_dataset_id="MKT-123"
                        ),
                        classification=EvidenceClassification.COMPOSITE,
                        interpretation_level=InterpretationLevel.OBJECTIVE,
                        validity_status=ValidityStatus.ACTIVE,
                        evidence_data={},
                        event_id=event_id,
                        event_timestamp=current_cluster[-1].timestamp,
                        trigger_rule="EqualLowDetector",
                        trigger_evidence=current_cluster[-1].anchor_id,
                        affected_state_ids=[],
                        causal_events=[],
                        severity="INFO",
                        sequence_number=1,
                        anchor_ids=anchor_ids,
                        anchor_count=len(anchor_ids),
                        average_price=avg_price,
                        price_variance=variance,
                        confidence_inputs=[]
                    )
                    events.append(event)
                    
        return events
