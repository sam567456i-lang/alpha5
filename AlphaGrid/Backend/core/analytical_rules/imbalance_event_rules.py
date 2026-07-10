from typing import List, Dict, Any
from datetime import datetime
from Backend.core.evidence_dtos.base import LineageRecord, EventLifecycleState
from Backend.core.evidence_dtos.imbalance_events import PartialFillEvent, FullFillEvent, TriggerSource
from Backend.core.evidence_dtos.imbalance import ImbalanceDirection

class ImbalanceEventEngine:
    """
    CQRS Event Engine.
    Only answers "What happened?" by observing price intersection with Imbalance bounds.
    NEVER mutates the ImbalanceObject itself.
    """
    def __init__(self, rule_id: str = "RULE-IMB-EVT-001"):
        self.rule_id = rule_id

    def scan_penetration(self, current_tick: Dict[str, Any], imbalance_object: Any) -> List[Any]:
        events = []
        price = current_tick.get("price", 0.0)
        timestamp = current_tick.get("timestamp", datetime.now())
        
        uuid = getattr(imbalance_object, "imbalance_uuid", "unknown")
        upper = getattr(imbalance_object, "upper_bound", 0.0)
        lower = getattr(imbalance_object, "lower_bound", 0.0)
        height = getattr(imbalance_object, "height", 1.0)
        direction = getattr(imbalance_object, "direction", ImbalanceDirection.NEUTRAL)
        
        if height == 0:
            return events

        # Bullish FVG (Price falling into it from above)
        if direction == ImbalanceDirection.BULLISH:
            if price < upper and price >= lower:
                penetration = upper - price
                fill_pct = (penetration / height) * 100.0
                
                evt = PartialFillEvent(
                    event_id=f"evt_partfill_{timestamp.timestamp()}",
                    event_type="PartialFill",
                    trigger_time=timestamp,
                    trigger_evidence=current_tick,
                    trigger_object_uuids=[uuid],
                    source_object_revisions={},
                    triggering_bar_timestamp=timestamp,
                    confidence=1.0,
                    event_lifecycle=EventLifecycleState.FIRED,
                    imbalance_uuid=uuid,
                    trigger_source=TriggerSource.TICK,
                    trigger_revisions={"rule_version": self.rule_id},
                    measured_price=price,
                    fill_percent_observed=fill_pct,
                    penetration_depth_observed=penetration,
                    lineage=LineageRecord(
                        platform="Platform10",
                        family="ImbalanceEvents",
                        capability="PenetrationScan",
                        source_dto_uuids=[uuid],
                        source_rule_ids=[self.rule_id],
                        source_engine_id="ImbalanceEventEngine",
                        parent_object_uuids=[],
                        source_revision="1.0.0",
                        version="1.0.0",
                        replay_id="",
                        timestamp=timestamp
                    )
                )
                events.append(evt)
            elif price < lower:
                evt = FullFillEvent(
                    event_id=f"evt_fullfill_{timestamp.timestamp()}",
                    event_type="FullFill",
                    trigger_time=timestamp,
                    trigger_evidence=current_tick,
                    trigger_object_uuids=[uuid],
                    source_object_revisions={},
                    triggering_bar_timestamp=timestamp,
                    confidence=1.0,
                    event_lifecycle=EventLifecycleState.FIRED,
                    imbalance_uuid=uuid,
                    trigger_source=TriggerSource.TICK,
                    trigger_revisions={"rule_version": self.rule_id},
                    measured_price=price,
                    lineage=LineageRecord(
                        platform="Platform10",
                        family="ImbalanceEvents",
                        capability="PenetrationScan",
                        source_dto_uuids=[uuid],
                        source_rule_ids=[self.rule_id],
                        source_engine_id="ImbalanceEventEngine",
                        parent_object_uuids=[],
                        source_revision="1.0.0",
                        version="1.0.0",
                        replay_id="",
                        timestamp=timestamp
                    )
                )
                events.append(evt)
                
        return events
