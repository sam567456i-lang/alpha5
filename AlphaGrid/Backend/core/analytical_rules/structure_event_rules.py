from typing import List, Dict, Any
from datetime import datetime
from Backend.core.evidence_dtos.base import LineageRecord, ObjectRelationship, RelationshipType, Cardinality, EventLifecycleState
from Backend.core.evidence_dtos.structure_events import BOSEvent, TransitionDirection, ConfirmationStatus

class StructureEventExtractionRule:
    """
    Scans incoming OHLC against certified StructureObjects to emit transitions (BOS, CHOCH).
    """
    def __init__(self, rule_id: str = "RULE-EVT-STRUC-001"):
        self.rule_id = rule_id

    def extract_bos(self, current_tick: Dict[str, Any], structure_objects: List[Any]) -> List[Any]:
        events = []
        price = current_tick.get("price", 0.0)
        timestamp = current_tick.get("timestamp", datetime.now())

        for obj in structure_objects:
            obj_uuid = getattr(getattr(obj, "identity", None), "uuid", "unknown_struc")
            obj_rev = getattr(obj, "operational_revision", 1)
            
            upper_bound = getattr(obj, "upper_bound", None)
            lower_bound = getattr(obj, "lower_bound", None)

            if upper_bound is not None and price > upper_bound:
                # Upward BOS
                event = BOSEvent(
                    event_id=f"evt_bos_{timestamp.timestamp()}_{obj_uuid}",
                    event_type="BOS",
                    trigger_time=timestamp,
                    trigger_evidence=current_tick,
                    trigger_object_uuids=[obj_uuid],
                    source_object_revisions={obj_uuid: obj_rev},
                    triggering_bar_timestamp=timestamp,
                    confidence=1.0,
                    event_lifecycle=EventLifecycleState.FIRED,
                    previous_structure_uuid=obj_uuid,
                    triggering_boundary_uuid=obj_uuid,
                    triggering_price=price,
                    transition_direction=TransitionDirection.ASCENDING,
                    confirmation_status=ConfirmationStatus.PENDING,
                    lineage=LineageRecord(
                        platform="Platform10",
                        family="StructureEvents",
                        capability="StructureBreak",
                        source_dto_uuids=[obj_uuid],
                        source_rule_ids=[self.rule_id],
                        source_engine_id="StructureEventEngine",
                        parent_object_uuids=[],
                        source_revision="1.0.0",
                        version="1.0.0",
                        replay_id="",
                        timestamp=timestamp
                    ),
                    relationships=[
                        ObjectRelationship(
                            source_uuid=f"evt_bos_{timestamp.timestamp()}_{obj_uuid}",
                            target_uuid=obj_uuid,
                            relationship_type=RelationshipType.REFERENCES,
                            cardinality=Cardinality.MANY_TO_ONE,
                            confidence=1.0
                        )
                    ]
                )
                events.append(event)
                
            elif lower_bound is not None and price < lower_bound:
                # Downward BOS
                event = BOSEvent(
                    event_id=f"evt_bos_{timestamp.timestamp()}_{obj_uuid}",
                    event_type="BOS",
                    trigger_time=timestamp,
                    trigger_evidence=current_tick,
                    trigger_object_uuids=[obj_uuid],
                    source_object_revisions={obj_uuid: obj_rev},
                    triggering_bar_timestamp=timestamp,
                    confidence=1.0,
                    event_lifecycle=EventLifecycleState.FIRED,
                    previous_structure_uuid=obj_uuid,
                    triggering_boundary_uuid=obj_uuid,
                    triggering_price=price,
                    transition_direction=TransitionDirection.DESCENDING,
                    confirmation_status=ConfirmationStatus.PENDING,
                    lineage=LineageRecord(
                        platform="Platform10",
                        family="StructureEvents",
                        capability="StructureBreak",
                        source_dto_uuids=[obj_uuid],
                        source_rule_ids=[self.rule_id],
                        source_engine_id="StructureEventEngine",
                        parent_object_uuids=[],
                        source_revision="1.0.0",
                        version="1.0.0",
                        replay_id="",
                        timestamp=timestamp
                    )
                )
                events.append(event)

        return events
