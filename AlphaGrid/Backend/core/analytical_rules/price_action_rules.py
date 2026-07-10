from typing import List, Dict, Any, Optional
from datetime import datetime
from Backend.core.evidence_dtos.base import LineageRecord, PlatformIdentity
from Backend.core.evidence_dtos.price_action import Doji, NR4, Engulfing

class PriceActionEngine:
    """
    Extracts purely geometric candlestick objects directly from OHLC.
    Asserts mathematical realities. Emits ZERO opinions.
    """
    def __init__(self, rule_id: str = "RULE-PA-001"):
        self.rule_id = rule_id

    def extract_single_candle(self, bar: Dict[str, Any], atr: float) -> List[Any]:
        events = []
        high = bar.get('high', 0.0)
        low = bar.get('low', 0.0)
        open_p = bar.get('open', 0.0)
        close = bar.get('close', 0.0)
        timestamp = bar.get('timestamp', datetime.now())
        
        spread = high - low
        body = abs(open_p - close)
        
        if spread > 0:
            # Doji Logic: Body is less than 5% of the total spread
            if body / spread <= 0.05:
                doji = Doji(
                    identity=PlatformIdentity(owner_family="PriceAction", uuid=f"doji_{timestamp.timestamp()}"),
                    lineage=self._build_lineage(timestamp, "DojiDetection"),
                    pa_uuid=f"doji_{timestamp.timestamp()}",
                    member_bar_timestamps=[timestamp.timestamp()],
                    geometric_upper_bound=high,
                    geometric_lower_bound=low,
                    open_close_distance=body
                )
                events.append(doji)
        return events

    def extract_two_candle(self, bar1: Dict[str, Any], bar2: Dict[str, Any]) -> List[Any]:
        events = []
        
        o1, c1, h1, l1 = bar1.get('open', 0.0), bar1.get('close', 0.0), bar1.get('high', 0.0), bar1.get('low', 0.0)
        o2, c2, h2, l2 = bar2.get('open', 0.0), bar2.get('close', 0.0), bar2.get('high', 0.0), bar2.get('low', 0.0)
        ts2 = bar2.get('timestamp', datetime.now())
        ts1 = bar1.get('timestamp', ts2)
        
        body1_top = max(o1, c1)
        body1_bot = min(o1, c1)
        body2_top = max(o2, c2)
        body2_bot = min(o2, c2)
        
        # Engulfing Logic: Bar 2 body completely engulfs Bar 1 body
        if body2_top > body1_top and body2_bot < body1_bot:
            eng = Engulfing(
                identity=PlatformIdentity(owner_family="PriceAction", uuid=f"engulf_{ts2.timestamp()}"),
                lineage=self._build_lineage(ts2, "EngulfingDetection"),
                pa_uuid=f"engulf_{ts2.timestamp()}",
                member_bar_timestamps=[ts1.timestamp(), ts2.timestamp()],
                geometric_upper_bound=max(h1, h2),
                geometric_lower_bound=min(l1, l2),
                engulfed_percentage=100.0
            )
            events.append(eng)
            
        return events

    def extract_range_patterns(self, lookback_bars: List[Dict[str, Any]]) -> List[Any]:
        events = []
        if len(lookback_bars) < 4:
            return events
            
        b1, b2, b3, b4 = lookback_bars[-4], lookback_bars[-3], lookback_bars[-2], lookback_bars[-1]
        
        r1 = b1.get('high', 0.0) - b1.get('low', 0.0)
        r2 = b2.get('high', 0.0) - b2.get('low', 0.0)
        r3 = b3.get('high', 0.0) - b3.get('low', 0.0)
        r4 = b4.get('high', 0.0) - b4.get('low', 0.0)
        
        ts4 = b4.get('timestamp', datetime.now())
        
        # NR4 Logic: Bar 4 range is the narrowest of the last 4
        if r4 < r1 and r4 < r2 and r4 < r3:
            nr4 = NR4(
                identity=PlatformIdentity(owner_family="PriceAction", uuid=f"nr4_{ts4.timestamp()}"),
                lineage=self._build_lineage(ts4, "NR4Detection"),
                pa_uuid=f"nr4_{ts4.timestamp()}",
                member_bar_timestamps=[b.get('timestamp', ts4).timestamp() for b in lookback_bars[-4:]],
                geometric_upper_bound=b4.get('high', 0.0),
                geometric_lower_bound=b4.get('low', 0.0),
                range_value=r4
            )
            events.append(nr4)
            
        return events

    def _build_lineage(self, timestamp: datetime, cap: str) -> LineageRecord:
        return LineageRecord(
            platform="Platform10",
            family="PriceAction",
            capability=cap,
            source_dto_uuids=[],
            source_rule_ids=[self.rule_id],
            source_engine_id="PriceActionEngine",
            parent_object_uuids=[],
            source_revision="1.0.0",
            version="1.0.0",
            replay_id="",
            timestamp=timestamp
        )
