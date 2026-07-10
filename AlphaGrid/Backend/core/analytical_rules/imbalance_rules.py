from typing import List, Dict, Any
from datetime import datetime
from Backend.core.evidence_dtos.base import LineageRecord, PlatformIdentity
from Backend.core.evidence_dtos.imbalance import FVG, ImbalanceLifecycleState

class ImbalanceExtractionRule:
    """
    Extracts Imbalance Objects purely from Price/Time (Geometry) data.
    Strictly forbids dependency on Institutional Zones.
    """
    def __init__(self, rule_id: str = "RULE-IMB-EXT-001"):
        self.rule_id = rule_id

    def extract_fvg(self, bar1: Dict[str, Any], bar2: Dict[str, Any], bar3: Dict[str, Any], timestamp: datetime) -> List[FVG]:
        """
        Calculates a standard 3-bar Fair Value Gap.
        Returns empty list if no gap exists.
        """
        events = []
        
        # Bullish FVG: Bar 1 High < Bar 3 Low
        if bar1['high'] < bar3['low']:
            lower_bound = bar1['high']
            upper_bound = bar3['low']
            height = upper_bound - lower_bound
            
            fvg = FVG(
                identity=PlatformIdentity(owner_family="ImbalanceObjects", uuid=f"fvg_bull_{timestamp.timestamp()}"),
                lineage=LineageRecord(
                    platform="Platform10",
                    family="ImbalanceObjects",
                    capability="FVGExtraction",
                    source_dto_uuids=[], # In a real system, these point to OHLC Tick UUIDs
                    source_rule_ids=[self.rule_id],
                    source_engine_id="ImbalanceEngine",
                    parent_object_uuids=[],
                    source_revision="1.0.0",
                    version="1.0.0",
                    replay_id="",
                    timestamp=timestamp
                ),
                imbalance_uuid=f"fvg_bull_{timestamp.timestamp()}",
                upper_bound=upper_bound,
                lower_bound=lower_bound,
                width=1.0, # Standard 1 bar width conceptually
                height=height,
                duration_bars=3,
                fill_percent=0.0,
                remaining_percent=1.0,
                lifecycle_state=ImbalanceLifecycleState.ACTIVE
            )
            events.append(fvg)
            
        # Bearish FVG: Bar 1 Low > Bar 3 High
        elif bar1['low'] > bar3['high']:
            upper_bound = bar1['low']
            lower_bound = bar3['high']
            height = upper_bound - lower_bound
            
            fvg = FVG(
                identity=PlatformIdentity(owner_family="ImbalanceObjects", uuid=f"fvg_bear_{timestamp.timestamp()}"),
                lineage=LineageRecord(
                    platform="Platform10",
                    family="ImbalanceObjects",
                    capability="FVGExtraction",
                    source_dto_uuids=[],
                    source_rule_ids=[self.rule_id],
                    source_engine_id="ImbalanceEngine",
                    parent_object_uuids=[],
                    source_revision="1.0.0",
                    version="1.0.0",
                    replay_id="",
                    timestamp=timestamp
                ),
                imbalance_uuid=f"fvg_bear_{timestamp.timestamp()}",
                upper_bound=upper_bound,
                lower_bound=lower_bound,
                width=1.0,
                height=height,
                duration_bars=3,
                fill_percent=0.0,
                remaining_percent=1.0,
                lifecycle_state=ImbalanceLifecycleState.ACTIVE
            )
            events.append(fvg)
            
        return events
