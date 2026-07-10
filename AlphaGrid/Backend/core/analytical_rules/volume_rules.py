from typing import List, Dict, Any, Optional
from datetime import datetime
from Backend.core.evidence_dtos.base import LineageRecord, PlatformIdentity
from Backend.core.evidence_dtos.volume_analytics import (
    ClimaxVolume, DryUpVolume, BuyingPressure, SellingPressure
)

class VolumeAnalyticsEngine:
    """
    Extracts pure Volume Objects directly from OHLCV and statistical baseline data.
    """
    def __init__(self, rule_id: str = "RULE-VOL-001"):
        self.rule_id = rule_id

    def analyze_volume(
        self, current_bar: Dict[str, Any], avg_volume: float, std_volume: float, timestamp: datetime
    ) -> List[Any]:
        """
        Takes the current OHLCV bar and computes exact relative volume and pressure.
        avg_volume and std_volume must be supplied by the upstream Statistics Engine.
        """
        events = []
        vol = current_bar.get("volume", None)
        
        if vol is None:
            raise ValueError("Volume Analytics Engine requires the 'volume' field in OHLCV data.")

        # Protection against div by zero on first bars
        if std_volume == 0:
            std_volume = 1.0
        if avg_volume == 0:
            avg_volume = 1.0

        sd_ratio = (vol - avg_volume) / std_volume
        rel_vol = vol / avg_volume

        # 1. Extrema Math
        if sd_ratio > 2.5:
            cv = ClimaxVolume(
                identity=PlatformIdentity(owner_family="VolumeAnalytics", uuid=f"climax_{timestamp.timestamp()}"),
                lineage=self._build_lineage(timestamp, "ClimaxDetection"),
                volume_uuid=f"climax_{timestamp.timestamp()}",
                measured_volume=vol,
                relative_volume_ratio=rel_vol,
                standard_deviations=sd_ratio
            )
            events.append(cv)
            
        elif sd_ratio < -2.0:
            du = DryUpVolume(
                identity=PlatformIdentity(owner_family="VolumeAnalytics", uuid=f"dryup_{timestamp.timestamp()}"),
                lineage=self._build_lineage(timestamp, "DryUpDetection"),
                volume_uuid=f"dryup_{timestamp.timestamp()}",
                measured_volume=vol,
                relative_volume_ratio=rel_vol,
                standard_deviations=sd_ratio
            )
            events.append(du)

        # 2. Pressure Math (Only applicable if high volume, e.g. > 1.5 SD)
        if sd_ratio > 1.5:
            high = current_bar.get("high", 0.0)
            low = current_bar.get("low", 0.0)
            close = current_bar.get("close", 0.0)
            
            spread = high - low
            if spread > 0:
                close_pct = (close - low) / spread
                
                if close_pct >= 0.75:
                    bp = BuyingPressure(
                        identity=PlatformIdentity(owner_family="VolumeAnalytics", uuid=f"bp_{timestamp.timestamp()}"),
                        lineage=self._build_lineage(timestamp, "BuyingPressureDetection"),
                        volume_uuid=f"bp_{timestamp.timestamp()}",
                        measured_volume=vol,
                        relative_volume_ratio=rel_vol,
                        close_percentage=close_pct
                    )
                    events.append(bp)
                elif close_pct <= 0.25:
                    sp = SellingPressure(
                        identity=PlatformIdentity(owner_family="VolumeAnalytics", uuid=f"sp_{timestamp.timestamp()}"),
                        lineage=self._build_lineage(timestamp, "SellingPressureDetection"),
                        volume_uuid=f"sp_{timestamp.timestamp()}",
                        measured_volume=vol,
                        relative_volume_ratio=rel_vol,
                        close_percentage=close_pct
                    )
                    events.append(sp)

        return events

    def _build_lineage(self, timestamp: datetime, cap: str) -> LineageRecord:
        return LineageRecord(
            platform="Platform10",
            family="VolumeAnalytics",
            capability=cap,
            source_dto_uuids=[], # In real implementation, maps back to exact OHLCV UUID
            source_rule_ids=[self.rule_id],
            source_engine_id="VolumeAnalyticsEngine",
            parent_object_uuids=[],
            source_revision="1.0.0",
            version="1.0.0",
            replay_id="",
            timestamp=timestamp
        )
