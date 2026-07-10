from typing import List, Dict, Any, Tuple
from datetime import datetime
from Backend.core.evidence_dtos.base import LineageRecord, PlatformIdentity
from Backend.core.evidence_dtos.institutional_zones import (
    BullishOrderBlock, BearishOrderBlock, ZoneValidity, ZoneFreshness, MitigationState
)
from Backend.core.evidence_dtos.structure_events import BOSEvent
from Backend.core.evidence_dtos.structure import StructuralBoundaryObject

class InstitutionalZoneConstructionRule:
    """
    Constructs Institutional Zones purely by consuming upstream Events and Objects.
    Never calculates BOS or Sweeps natively.
    """
    def __init__(self, rule_id: str = "RULE-ZONE-CON-001"):
        self.rule_id = rule_id

    def build_order_block(self, bos_event: Any, structure_boundary: Any, liquidity_object: Any, timestamp: datetime) -> Any:
        """
        Creates an Order Block perfectly anchored to a BOS Event.
        """
        if not isinstance(bos_event, BOSEvent):
            raise ValueError("Institutional Zones require a valid Structure Event (e.g., BOS) to instantiate.")

        if not structure_boundary:
            raise ValueError("Institutional Zones require a valid Structural Boundary.")
            
        if not liquidity_object:
            raise ValueError("Institutional Zones require a valid Liquidity Object reference.")

        bos_uuid = getattr(bos_event, "event_id", "unknown_bos")
        struc_uuid = getattr(getattr(structure_boundary, "identity", None), "uuid", "unknown_struc")
        liq_uuid = getattr(getattr(liquidity_object, "identity", None), "uuid", "unknown_liq")

        upper_uuid = struc_uuid # In reality, references the actual boundary obj
        lower_uuid = struc_uuid

        ob_class = BullishOrderBlock if bos_event.transition_direction.value == "ASCENDING" else BearishOrderBlock

        return ob_class(
            identity=PlatformIdentity(owner_family="InstitutionalZones", uuid=f"ob_{bos_uuid}_{timestamp.timestamp()}"),
            lineage=LineageRecord(
                platform="Platform10",
                family="InstitutionalZones",
                capability="OrderBlockConstruction",
                source_dto_uuids=[bos_uuid, struc_uuid, liq_uuid],
                source_rule_ids=[self.rule_id],
                source_engine_id="InstitutionalZoneEngine",
                parent_object_uuids=[],
                source_revision="1.0.0",
                version="1.0.0",
                replay_id="",
                timestamp=timestamp
            ),
            zone_uuid=f"ob_{bos_uuid}_{timestamp.timestamp()}",
            upper_boundary_uuid=upper_uuid,
            lower_boundary_uuid=lower_uuid,
            origin_structure_uuids=[struc_uuid],
            origin_event_uuids=[bos_uuid],
            origin_liquidity_uuids=[liq_uuid],
            validity=ZoneValidity.VALID,
            freshness=ZoneFreshness.FRESH,
            mitigation_state=MitigationState.UNMITIGATED
        )
