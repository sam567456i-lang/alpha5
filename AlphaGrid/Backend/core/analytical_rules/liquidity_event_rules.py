from typing import List, Dict, Any
from datetime import datetime
from Backend.core.evidence_dtos.base import LineageRecord, ObjectRelationship, RelationshipType, Cardinality
from Backend.core.evidence_dtos.liquidity_events import SweepEvent, TouchEvent

class LiquidityEventExtractionRule:
    """
    Scans incoming OHLC data against Certified Liquidity Objects.
    Detects Touch, Sweep, Break, etc.
    """
    def __init__(self, rule_id: str = "RULE-EVT-LIQ-001"):
        self.rule_id = rule_id

    def _create_lineage(self, current_timestamp: datetime) -> LineageRecord:
        return LineageRecord(
            platform="Platform10",
            family="LiquidityEvents",
            capability="EventExtraction",
            source_dto_uuids=[], 
            source_rule_ids=[self.rule_id],
            source_engine_id="LiquidityEventEngine",
            parent_object_uuids=[],
            source_revision="1.0.0",
            version="1.0.0",
            replay_id="",
            timestamp=current_timestamp
        )

    def extract(self, current_tick: Dict[str, Any], active_objects: List[Any]) -> List[Any]:
        events = []
        price = current_tick.get("price", 0.0)
        timestamp = current_tick.get("timestamp", datetime.now())
        
        for obj in active_objects:
            # For this test, we assume objects are Boundaries (like Range or Reference Pools)
            # which have upper_bound and lower_bound, or simple objects with a price.
            obj_price = getattr(obj, "price", getattr(obj, "upper_bound", 0.0))
            obj_uuid = getattr(getattr(obj, "identity", None), "uuid", "unknown")
            obj_rev = getattr(obj, "operational_revision", 1)
            
            # Simple Touch Detection logic
            if abs(price - obj_price) < 0.001:
                event = TouchEvent(
                    event_id=f"evt_{timestamp.timestamp()}_{obj_uuid}",
                    event_type="TOUCH",
                    trigger_time=timestamp,
                    trigger_evidence=current_tick,
                    trigger_object_uuids=[obj_uuid],
                    source_object_revisions={obj_uuid: obj_rev},
                    triggering_bar_timestamp=timestamp,
                    confidence=1.0,
                    lineage=self._create_lineage(timestamp),
                    relationships=[
                        ObjectRelationship(
                            source_uuid=f"evt_{timestamp.timestamp()}_{obj_uuid}",
                            target_uuid=obj_uuid,
                            relationship_type=RelationshipType.REFERENCES,
                            cardinality=Cardinality.MANY_TO_ONE,
                            confidence=1.0
                        )
                    ]
                )
                events.append(event)
                
            # Simple Sweep Detection logic (overshoot slightly and reverse - simulated)
            elif price > obj_price and (price - obj_price) < 0.05:
                event = SweepEvent(
                    event_id=f"evt_swp_{timestamp.timestamp()}_{obj_uuid}",
                    event_type="SWEEP",
                    trigger_time=timestamp,
                    trigger_evidence=current_tick,
                    trigger_object_uuids=[obj_uuid],
                    source_object_revisions={obj_uuid: obj_rev},
                    triggering_bar_timestamp=timestamp,
                    confidence=0.9,
                    lineage=self._create_lineage(timestamp),
                    relationships=[
                        ObjectRelationship(
                            source_uuid=f"evt_swp_{timestamp.timestamp()}_{obj_uuid}",
                            target_uuid=obj_uuid,
                            relationship_type=RelationshipType.REFERENCES,
                            cardinality=Cardinality.MANY_TO_ONE,
                            confidence=1.0
                        )
                    ]
                )
                events.append(event)
                
        return events
