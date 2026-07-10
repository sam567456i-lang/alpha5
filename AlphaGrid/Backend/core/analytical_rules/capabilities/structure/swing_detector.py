from Backend.core.engine.evidence_quality import EvidenceQualityMetadata
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
from Backend.core.analytical_rules.capabilities.structure.swing_policy import SwingPolicy
from Backend.core.analytical_rules.dto.structure.swing_formation_event import SwingFormationEvent
from Backend.core.analytical_rules.dto.structure.swing_identity_dto import SwingIdentityDTO
from Backend.core.analytical_rules.utils.identity_factory import IdentityFactory
from Backend.core.analytical_rules.dto.evidence_identity_dto import EvidenceIdentityDTO
from Backend.core.analytical_rules.dto.evidence_metadata_dto import EvidenceMetadataDTO
from Backend.core.analytical_rules.dto.evidence_provenance_dto import EvidenceProvenanceDTO
from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification
from Backend.core.analytical_rules.dto.interpretation_level import InterpretationLevel
from Backend.core.analytical_rules.dto.validity_status import ValidityStatus

class SwingDetector:
    """
    Observes raw market data and applies a SwingPolicy to emit SwingFormationEvents.
    Strictly observes; maintains no state.
    """
    def __init__(self, policy: SwingPolicy):
        self.policy = policy

    def detect(self, ohlcv_data: List[Dict[str, Any]]) -> List[SwingFormationEvent]:
        events = []
        for i in range(len(ohlcv_data)):
            candle = ohlcv_data[i]
            timestamp = candle["timestamp"]
            
            if self.policy.is_swing_high(i, ohlcv_data):
                events.append(self._create_event("high", candle["high"], timestamp, i))
                
            if self.policy.is_swing_low(i, ohlcv_data):
                events.append(self._create_event("low", candle["low"], timestamp, i))
                
        return events

    def _create_event(self, direction: str, price: float, timestamp: str, index: int) -> SwingFormationEvent:
        conf_window = getattr(self.policy, "left_confirmation", 2)
        
        geometry_fingerprint = IdentityFactory.generate_geometry_fingerprint(
            price=price,
            timestamp=timestamp,
            direction=direction,
            timeframe="1h",
            symbol="TEST"
        )
        
        # Deterministic IDs
        event_id = IdentityFactory.generate_event_id("SwingFormationEvent", geometry_fingerprint, self.policy.policy_checksum)
        
        swing_identity = SwingIdentityDTO(
            id=event_id,
            symbol="TEST",
            timeframe="1h",
            timestamp=timestamp,
            price=price,
            direction=direction,
            policy_id=self.policy.policy_id,
            policy_version="1.0.0",
            policy_checksum=self.policy.policy_checksum,
            geometry_fingerprint=geometry_fingerprint
        )
        
        return SwingFormationEvent(
            identity=EvidenceIdentityDTO(
                evidence_id=event_id, 
                evidence_type="SwingFormationEvent",
                capability_id="CAP-STRUCTURE-01",
                ontology_id="ONT-SWING-EVENT"
            ),
            metadata=EvidenceMetadataDTO(
                schema_version="1.0.0",
                rule_version="1.0.0",
                rule_checksum="none",
                registry_checksum="none",
                sdk_version="1.0.0",
                planner_version="1.0.0",
                fingerprint="none",
                custom_tags={}
            ),
            provenance=EvidenceProvenanceDTO(
                producer_rule="SwingDetector",
                execution_mode="Standard",
                execution_timestamp=timestamp,
                source_evidence_ids=[],
                market_dataset_id="MKT-123"
            ),
            classification=EvidenceClassification.PRIMITIVE,
            interpretation_level=InterpretationLevel.OBJECTIVE,
            validity_status=ValidityStatus.GENERATED,
            evidence_data={},
            quality=EvidenceQualityMetadata(confidence=1.0, coverage=1.0, freshness=0.0, latency=0.0, source_quality=1.0, sample_size=1, stability=1.0),
            superseded_by=None,
            event_id=event_id,
            event_timestamp=timestamp,
            trigger_rule="SwingDetector",
            trigger_evidence="",
            affected_state_ids=[],
            causal_events=[],
            severity="info",
            sequence_number=index,
            confidence_inputs=[],
            swing=swing_identity
        )
