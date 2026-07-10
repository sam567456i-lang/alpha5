from typing import List, Dict, Any
from datetime import datetime, date
from Backend.core.evidence_dtos.liquidity import ReferenceLevel, ReferenceSource, ReferenceType
from Backend.core.evidence_dtos.base import PlatformIdentity, LineageRecord

class ReferenceLevelExtractionRule:
    """
    Extracts daily, weekly, monthly reference levels from OHLC data.
    """
    def __init__(self, rule_id: str = "RULE-REF-001"):
        self.rule_id = rule_id

    def extract(self, current_timestamp: datetime, historical_data: Dict[str, Any]) -> List[ReferenceLevel]:
        """
        historical_data is expected to contain pre-aggregated values like:
        {
            'previous_day': {'high': 105.0, 'low': 100.0, 'open': 101.0, 'date': '2026-07-08'},
            'previous_week': {'high': 110.0, 'low': 95.0, 'open': 96.0, 'date': '2026-W27'},
            'current_day': {'high': 106.0, 'low': 102.0, 'open': 102.5, 'date': '2026-07-09'}
        }
        """
        levels = []
        
        # Example extracting Previous Day High
        prev_day = historical_data.get('previous_day')
        if prev_day:
            levels.append(ReferenceLevel(
                identity=PlatformIdentity(owner_family="LiquidityObjects"),
                lineage=LineageRecord(
                    platform="Platform10",
                    family="LiquidityObjects",
                    capability="ReferenceLevel",
                    source_dto_uuids=[], 
                    source_rule_ids=[self.rule_id],
                    source_engine_id="ReferenceLevelEngine",
                    parent_object_uuids=[],
                    source_revision="1.0.0",
                    version="1.0.0",
                    replay_id="",
                    timestamp=current_timestamp
                ),
                reference_source=ReferenceSource.CALENDAR,
                reference_type=ReferenceType.PREVIOUS_DAY_HIGH,
                price=prev_day['high'],
                interval_identifier=prev_day['date']
            ))
            
            levels.append(ReferenceLevel(
                identity=PlatformIdentity(owner_family="LiquidityObjects"),
                lineage=LineageRecord(
                    platform="Platform10",
                    family="LiquidityObjects",
                    capability="ReferenceLevel",
                    source_dto_uuids=[], 
                    source_rule_ids=[self.rule_id],
                    source_engine_id="ReferenceLevelEngine",
                    parent_object_uuids=[],
                    source_revision="1.0.0",
                    version="1.0.0",
                    replay_id="",
                    timestamp=current_timestamp
                ),
                reference_source=ReferenceSource.CALENDAR,
                reference_type=ReferenceType.PREVIOUS_DAY_LOW,
                price=prev_day['low'],
                interval_identifier=prev_day['date']
            ))

        return levels

class SwingLiquiditySelectionRule:
    """
    Selection Phase: Determines which SwingEvidence objects qualify to become SwingLiquidity.
    """
    def __init__(self, rule_id: str = "RULE-SWI-LIQ-SEL-001"):
        self.rule_id = rule_id

    def select(self, available_swings: List[Any]) -> List[Any]:
        # Filter logic to only select significant swings
        # In real code, 'available_swings' would be typed as SwingEvidence
        selected = []
        for swing in available_swings:
            # Example condition: Must be at least a minor swing (hierarchy_level >= 1)
            if getattr(swing, 'hierarchy_level', 0) >= 1:
                selected.append(swing)
        return selected

class SwingLiquidityConstructionRule:
    """
    Construction Phase: Builds the final SwingLiquidityObject.
    """
    def __init__(self, rule_id: str = "RULE-SWI-LIQ-CON-001"):
        self.rule_id = rule_id

    def construct(self, selected_swings: List[Any], current_timestamp: datetime) -> List[Any]:
        from Backend.core.evidence_dtos.liquidity import SwingLiquidityObject, SwingLiquidityEvidence
        
        objects = []
        for swing in selected_swings:
            evidence = SwingLiquidityEvidence(
                price=getattr(swing, 'price', 0.0),
                tolerance=getattr(swing, 'tolerance', 0.0),
                hierarchy_level=getattr(swing, 'hierarchy_level', 0),
                source_swing_uuid=getattr(swing, 'identity', {}).get('uuid', "")
            )
            
            obj = SwingLiquidityObject(
                identity=PlatformIdentity(owner_family="LiquidityObjects"),
                lineage=LineageRecord(
                    platform="Platform10",
                    family="LiquidityObjects",
                    capability="SwingLiquidity",
                    source_dto_uuids=[evidence.source_swing_uuid], 
                    source_rule_ids=[self.rule_id],
                    source_engine_id="SwingLiquidityEngine",
                    parent_object_uuids=[],
                    source_revision="1.0.0",
                    version="1.0.0",
                    replay_id="",
                    timestamp=current_timestamp
                ),
                evidence=evidence
            )
            objects.append(obj)
            
        return objects

