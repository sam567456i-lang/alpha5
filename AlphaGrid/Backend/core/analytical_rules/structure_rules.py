from typing import List, Dict, Any, Tuple
from datetime import datetime
from Backend.core.evidence_dtos.base import LineageRecord, PlatformIdentity
from Backend.core.evidence_dtos.structure import (
    StructuralLegObject, StructuralState, InternalStructureObject, ExternalStructureObject, StructureHierarchyObject
)

class StructureSelectionRule:
    """
    Selects source geometry (Swings, Ranges) to feed into Structure computation.
    Strictly forbids dependency on temporal Liquidity Events.
    """
    def select_swings(self, objects: List[Any]) -> List[Any]:
        # Filter logic to ensure only pure Geometry/Swings are retrieved
        return [obj for obj in objects if getattr(obj, "family", "") == "Swing"]

class StructureConstructionRule:
    """
    Constructs the canonical 9 structural objects from objective geometry inputs.
    """
    def __init__(self, rule_id: str = "RULE-STRUC-CON-001"):
        self.rule_id = rule_id

    def build_leg(self, swing_a: Any, swing_b: Any, timestamp: datetime) -> StructuralLegObject:
        """Constructs a Structural Leg bridging two exact swings."""
        uuid_a = getattr(getattr(swing_a, "identity", None), "uuid", "unknown_a")
        uuid_b = getattr(getattr(swing_b, "identity", None), "uuid", "unknown_b")
        price_a = getattr(swing_a, "price", 0.0)
        price_b = getattr(swing_b, "price", 0.0)
        
        state = StructuralState.ASCENDING if price_b > price_a else StructuralState.DESCENDING

        return StructuralLegObject(
            identity=PlatformIdentity(owner_family="StructureObjects", uuid=f"leg_{uuid_a}_{uuid_b}"),
            lineage=LineageRecord(
                platform="Platform10",
                family="StructureObjects",
                capability="StructureConstruction",
                source_dto_uuids=[uuid_a, uuid_b],  # DEEP PROVENANCE TRACING
                source_rule_ids=[self.rule_id],
                source_engine_id="StructureEngine",
                parent_object_uuids=[],
                source_revision="1.0.0",
                version="1.0.0",
                replay_id="",
                timestamp=timestamp
            ),
            structural_state=state,
            start_swing_uuid=uuid_a,
            end_swing_uuid=uuid_b,
            price_delta=price_b - price_a
        )

    def build_hierarchy(self, internal_obj: InternalStructureObject, external_obj: ExternalStructureObject, timestamp: datetime) -> StructureHierarchyObject:
        """Constructs a vertical tree mapping ensuring Internal <= External bounds."""
        int_uuid = getattr(getattr(internal_obj, "identity", None), "uuid", "int_uuid")
        ext_uuid = getattr(getattr(external_obj, "identity", None), "uuid", "ext_uuid")

        # Mathematical verification of bounds before emitting hierarchy
        if (internal_obj.upper_bound > external_obj.upper_bound) or (internal_obj.lower_bound < external_obj.lower_bound):
            raise ValueError(f"Hierarchy Violation: Internal bounds ({internal_obj.lower_bound}, {internal_obj.upper_bound}) exceed External bounds ({external_obj.lower_bound}, {external_obj.upper_bound}).")
            
        return StructureHierarchyObject(
            identity=PlatformIdentity(owner_family="StructureObjects", uuid=f"hier_{ext_uuid}_{int_uuid}"),
            lineage=LineageRecord(
                platform="Platform10",
                family="StructureObjects",
                capability="StructureHierarchy",
                source_dto_uuids=[int_uuid, ext_uuid],
                source_rule_ids=[self.rule_id],
                source_engine_id="StructureEngine",
                parent_object_uuids=[],
                source_revision="1.0.0",
                version="1.0.0",
                replay_id="",
                timestamp=timestamp
            ),
            structural_state=StructuralState.NESTED,
            parent_uuid=ext_uuid,
            child_uuids=[int_uuid]
        )
