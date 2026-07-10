from typing import List, Optional
from datetime import datetime
from Backend.core.evidence_dtos.base import LineageRecord, PlatformIdentity
from Backend.core.evidence_dtos.market_profile import ValueArea, Excess
from Backend.core.evidence_dtos.amt import Rejection

class AMTEngine:
    """
    Auction Market Theory Engine.
    Exclusively consumes CERTIFIED Profile Objects (ValueArea, Excess).
    Never interacts with raw Histograms.
    """
    def __init__(self, rule_id: str = "RULE-AMT-001"):
        self.rule_id = rule_id

    def evaluate_rejection(self, current_price: float, prior_va: ValueArea, current_excess: Optional[Excess], timestamp: datetime) -> List[Rejection]:
        """
        If price tests a prior Value Area and immediately generates an Excess tail, 
        it is mathematically classified as Rejection.
        """
        events = []
        
        if not current_excess:
            return events
            
        # Is price testing the VA?
        testing_vah = abs(current_price - prior_va.vah_price) < 5.0 # Tolerance logic
        testing_val = abs(current_price - prior_va.val_price) < 5.0
        
        # Rejection from VAH = Selling Tail (not buying tail)
        # Rejection from VAL = Buying Tail
        if (testing_vah and not current_excess.is_buying_tail) or (testing_val and current_excess.is_buying_tail):
            rej = Rejection(
                identity=PlatformIdentity(owner_family="AMT", uuid=f"rej_{timestamp.timestamp()}"),
                lineage=self._build_lineage(timestamp, "RejectionExtraction"),
                amt_uuid=f"rej_{timestamp.timestamp()}",
                rejected_price_level=current_price,
                excess_tail_length=current_excess.tail_length
            )
            events.append(rej)
            
        return events

    def _build_lineage(self, timestamp: datetime, cap: str) -> LineageRecord:
        return LineageRecord(
            platform="Platform10",
            family="AMT",
            capability=cap,
            source_dto_uuids=[],
            source_rule_ids=[self.rule_id],
            source_engine_id="AMTEngine",
            parent_object_uuids=[],
            source_revision="1.0.0",
            version="1.0.0",
            replay_id="",
            timestamp=timestamp
        )
