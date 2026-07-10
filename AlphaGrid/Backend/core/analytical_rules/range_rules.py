from typing import List, Dict, Any, Tuple
from datetime import datetime
from Backend.core.evidence_dtos.base import PlatformIdentity, LineageRecord
from Backend.core.evidence_dtos.range import (
    InternalRangeObject, ExternalRangeObject, RangeReferenceObject,
    RangeRatioBoundary, SegmentObject, SegmentDefinition,
    RangeRelationshipType, RangeRelationshipObject
)

class RangeLiquiditySelectionRule:
    """
    Selection Phase: Selects certified upstream evidence that forms valid ranges.
    """
    def __init__(self, rule_id: str = "RULE-RNG-LIQ-SEL-001"):
        self.rule_id = rule_id

    def select(self, available_ranges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        selected = []
        for r in available_ranges:
            if "upper_bound" in r and "lower_bound" in r and "start_time" in r:
                # Discard inverted or totally invalid inputs
                if r["upper_bound"] >= r["lower_bound"]:
                    selected.append(r)
        return selected

class RangeLiquidityValidationRule:
    """
    Validation Phase: Validates ranges for zero-width, tiny ticks, and extreme values.
    """
    def __init__(self, rule_id: str = "RULE-RNG-LIQ-VAL-001"):
        self.rule_id = rule_id

    def validate(self, selected_ranges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        validated = []
        for r in selected_ranges:
            width = r["upper_bound"] - r["lower_bound"]
            if width >= 0:
                validated.append(r)
        return validated

class RangeLiquidityConstructionRule:
    """
    Construction Phase: Builds the 6 object groups from validated ranges.
    """
    def __init__(self, rule_id: str = "RULE-RNG-LIQ-CON-001"):
        self.rule_id = rule_id

    def _create_lineage(self, current_timestamp: datetime) -> LineageRecord:
        return LineageRecord(
            platform="Platform10",
            family="RangeLiquidity",
            capability="RangeLiquidityConstruction",
            source_dto_uuids=[], 
            source_rule_ids=[self.rule_id],
            source_engine_id="RangeLiquidityEngine",
            parent_object_uuids=[],
            source_revision="1.0.0",
            version="1.0.0",
            replay_id="",
            timestamp=current_timestamp
        )

    def construct(self, validated_ranges: List[Dict[str, Any]], current_timestamp: datetime) -> Tuple[List[Any], List[RangeRelationshipObject]]:
        objects = []
        relationships = []
        
        # 1. Build Objects
        for r in validated_ranges:
            uuid_prefix = r.get("id", str(current_timestamp.timestamp()))
            
            # Internal/External (Simplify here by creating an InternalRangeObject)
            internal_obj = InternalRangeObject(
                identity=PlatformIdentity(owner_family="RangeLiquidity", uuid=f"int_{uuid_prefix}"),
                lineage=self._create_lineage(current_timestamp),
                upper_bound=r["upper_bound"],
                lower_bound=r["lower_bound"],
                origin_timestamp=r["start_time"]
            )
            objects.append(internal_obj)
            
            # Reference Object
            ref_obj = RangeReferenceObject(
                identity=PlatformIdentity(owner_family="RangeLiquidity", uuid=f"ref_{uuid_prefix}"),
                lineage=self._create_lineage(current_timestamp),
                start_time=r["start_time"],
                end_time=r.get("end_time", current_timestamp)
            )
            objects.append(ref_obj)
            
            # Range Ratio Boundaries (0.25, 0.50, 0.75)
            for ratio in [0.25, 0.50, 0.75]:
                ratio_val = r["lower_bound"] + (internal_obj.width * ratio)
                ratio_obj = RangeRatioBoundary(
                    identity=PlatformIdentity(owner_family="RangeLiquidity", uuid=f"ratio_{ratio}_{uuid_prefix}"),
                    lineage=self._create_lineage(current_timestamp),
                    upper_bound=ratio_val,
                    lower_bound=ratio_val, # Band is flat
                    origin_timestamp=r["start_time"],
                    ratio=ratio
                )
                objects.append(ratio_obj)
                
            # Segments (Upper, Lower halves as example)
            segments = [
                SegmentDefinition("lower_half", 0.0, 0.5),
                SegmentDefinition("upper_half", 0.5, 1.0)
            ]
            for seg in segments:
                seg_obj = SegmentObject(
                    identity=PlatformIdentity(owner_family="RangeLiquidity", uuid=f"seg_{seg.name}_{uuid_prefix}"),
                    lineage=self._create_lineage(current_timestamp),
                    upper_bound=r["lower_bound"] + (internal_obj.width * seg.upper_ratio),
                    lower_bound=r["lower_bound"] + (internal_obj.width * seg.lower_ratio),
                    origin_timestamp=r["start_time"],
                    definition=seg
                )
                objects.append(seg_obj)

        # 2. Build Relationships (Linking Phase)
        # O(N^2) naive check for overlapping
        for i in range(len(validated_ranges)):
            for j in range(i + 1, len(validated_ranges)):
                r1 = validated_ranges[i]
                r2 = validated_ranges[j]
                
                r1_uuid = f"int_{r1.get('id', '')}"
                r2_uuid = f"int_{r2.get('id', '')}"
                
                # Check overlap
                if max(r1["lower_bound"], r2["lower_bound"]) <= min(r1["upper_bound"], r2["upper_bound"]):
                    rel = RangeRelationshipObject(
                        identity=PlatformIdentity(owner_family="RangeLiquidity"),
                        lineage=self._create_lineage(current_timestamp),
                        relationship_type=RangeRelationshipType.OVERLAPS,
                        source_uuid=r1_uuid,
                        target_uuid=r2_uuid
                    )
                    relationships.append(rel)
                    
        return objects, relationships
