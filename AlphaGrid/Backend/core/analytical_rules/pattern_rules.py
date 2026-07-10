from typing import List, Dict, Any, Optional
from datetime import datetime
from Backend.core.evidence_dtos.base import LineageRecord, PlatformIdentity
from Backend.core.evidence_dtos.pattern_components import (
    DoubleTopPolicy, Peak, Neckline
)
from Backend.core.evidence_dtos.pattern_recognition import (
    DoubleTop, PatternLifecycleState
)

class PatternRecognitionEngine:
    """
    Extracts geometric multi-swing Patterns.
    Driven entirely by structural Policies, NEVER hardcoded opinions.
    """
    def __init__(self, rule_id: str = "RULE-PAT-001"):
        self.rule_id = rule_id

    def evaluate_double_top(
        self, 
        swing_high_1: Dict[str, Any], 
        swing_low: Dict[str, Any], 
        swing_high_2: Dict[str, Any], 
        policy: DoubleTopPolicy,
        timestamp: datetime
    ) -> List[Any]:
        """
        Evaluates a sequence of 3 swings (High -> Low -> High) to construct a DoubleTop.
        Must satisfy the injected DoubleTopPolicy geometric variance constraints.
        """
        events = []
        
        p1 = swing_high_1.get('price', 0.0)
        p2 = swing_high_2.get('price', 0.0)
        p_low = swing_low.get('price', 0.0)
        
        ts1 = swing_high_1.get('timestamp', timestamp.timestamp())
        ts2 = swing_high_2.get('timestamp', timestamp.timestamp())
        ts_low = swing_low.get('timestamp', timestamp.timestamp())
        
        # 1. Check Variance Constraint
        higher_peak = max(p1, p2)
        lower_peak = min(p1, p2)
        variance = (higher_peak - lower_peak) / higher_peak
        
        if variance > policy.max_peak_variance_pct:
            return events # Rejected by policy

        # 2. Check Neckline Depth
        depth = (higher_peak - p_low) / higher_peak
        if depth < policy.min_neckline_depth_pct:
            return events # Rejected by policy (too shallow to be a structural double top)
            
        # 3. Construct Components
        peak1_comp = Peak(component_uuid=f"peak1_{ts1}", price_level=p1, timestamp=ts1)
        peak2_comp = Peak(component_uuid=f"peak2_{ts2}", price_level=p2, timestamp=ts2)
        neckline_comp = Neckline(component_uuid=f"neck_{ts_low}", y_intercept=p_low, slope=0.0)
        
        # 4. Construct Pattern
        dt = DoubleTop(
            identity=PlatformIdentity(owner_family="PatternRecognition", uuid=f"dt_{timestamp.timestamp()}"),
            lineage=self._build_lineage(timestamp, "DoubleTopExtraction"),
            pattern_uuid=f"dt_{timestamp.timestamp()}",
            lifecycle_state=PatternLifecycleState.CANDIDATE,
            peak1=peak1_comp,
            peak2=peak2_comp,
            neckline=neckline_comp
        )
        
        dt.quality.geometric_error = variance # Expose the mathematical variance cleanly
        
        events.append(dt)
        return events

    def _build_lineage(self, timestamp: datetime, cap: str) -> LineageRecord:
        return LineageRecord(
            platform="Platform10",
            family="PatternRecognition",
            capability=cap,
            source_dto_uuids=[],
            source_rule_ids=[self.rule_id],
            source_engine_id="PatternRecognitionEngine",
            parent_object_uuids=[],
            source_revision="1.0.0",
            version="1.0.0",
            replay_id="",
            timestamp=timestamp
        )
