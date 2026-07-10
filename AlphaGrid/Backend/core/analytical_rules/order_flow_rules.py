from typing import Optional, List, Dict
from Backend.core.interfaces.market_data import Tick, Trade, MarketDataView
from Backend.core.interfaces.capabilities import FeedManifest, EngineCapabilityNegotiator, FeedCapability, CapabilityLevel
from Backend.core.evidence_dtos.base import PlatformIdentity, LineageRecord
from Backend.core.evidence_dtos.order_flow import (
    TradeClassificationPolicy, TradeClassificationRule, DeltaMeasurement, CumulativeDeltaMeasurement
)
from datetime import datetime

class OrderBookState:
    """O(1) incremental bid/ask depth updates."""
    def __init__(self):
        self.bids: Dict[float, float] = {}
        self.asks: Dict[float, float] = {}
        self.best_bid = 0.0
        self.best_ask = 0.0

    def update(self, price: float, size: float, is_bid: bool):
        if is_bid:
            self.bids[price] = size
            if size == 0:
                del self.bids[price]
            # Fast best bid tracking omitted for brevity
        else:
            self.asks[price] = size
            if size == 0:
                del self.asks[price]

class OrderFlowEngine:
    """
    Policy-driven Order Flow Engine with strict capability negotiation.
    """
    def __init__(self, feed_manifest: FeedManifest, policy: TradeClassificationPolicy):
        self.policy = policy
        self.negotiator = EngineCapabilityNegotiator("OrderFlowEngine", feed_manifest)
        self.book = OrderBookState()
        self.current_cvd = 0.0
        self.last_tick_price = 0.0
        
        # Negotiate Modules
        self.delta_capability = self.negotiator.negotiate_module("DeltaModule", required={FeedCapability.TRADE})
        self.iceberg_capability = self.negotiator.negotiate_module("IcebergModule", required={FeedCapability.LEVEL2})
        self.absorption_capability = self.negotiator.negotiate_module("AbsorptionModule", required={FeedCapability.LEVEL2})

    def process_trade(self, trade: Trade) -> Optional[DeltaMeasurement]:
        """Processes a single trade event incrementally."""
        # 1. Delta Calculation (Always runs if TRADE capability is met)
        if self.delta_capability == CapabilityLevel.UNSUPPORTED:
            return None
            
        is_buyer_initiated = self._classify_trade(trade)
        self.last_tick_price = trade.price
        
        bid_vol = 0.0
        ask_vol = 0.0
        if is_buyer_initiated:
            ask_vol = trade.size
        else:
            bid_vol = trade.size
            
        net_delta = ask_vol - bid_vol
        self.current_cvd += net_delta
        
        # We only output Delta if we only have Trades. 
        # Iceberg/Absorption logic would branch here based on self.iceberg_capability
        if self.iceberg_capability != CapabilityLevel.UNSUPPORTED:
            self._process_icebergs(trade)
            
        # Return strict Delta measurement for now
        return DeltaMeasurement(
            identity=PlatformIdentity(owner_family="OrderFlow"),
            lineage=LineageRecord("Platform10", "OrderFlow", "DeltaExtraction", [], [], "OrderFlowEngine", [], "1.0", "1.0", "", datetime.now()),
            bid_volume=bid_vol,
            ask_volume=ask_vol,
            net_delta=net_delta
        )
        
    def _classify_trade(self, trade: Trade) -> bool:
        if self.policy.rule == TradeClassificationRule.EXCHANGE_NATIVE:
            return trade.is_buyer_maker is False # Maker was seller, so buyer initiated
        if self.policy.rule == TradeClassificationRule.TICK_RULE:
            if trade.price > self.last_tick_price:
                return True
            elif trade.price < self.last_tick_price:
                return False
            # Tie breaker omitted for brevity
            return True
        return True
        
    def _process_icebergs(self, trade: Trade):
        # Implementation relying on Level 2 Order Book State
        pass
