import math
from typing import Dict
from Backend.market_data.pipeline import IDerivedDataGenerator
from Backend.core.events import CanonicalMarketEvent, EnrichedMarketEvent, DerivedMetrics

class SessionState:
    def __init__(self):
        self.open = 0.0
        self.high = 0.0
        self.low = float('inf')
        self.close = 0.0
        self.volume = 0.0
        self.prev_close = 0.0
        
    def update(self, price: float, volume: float):
        if self.open == 0.0:
            self.open = price
        self.prev_close = self.close
        if price > self.high:
            self.high = price
        if price < self.low:
            self.low = price
        self.close = price
        self.volume += volume

class DerivedDataGenerator(IDerivedDataGenerator):
    def __init__(self):
        self.sessions: Dict[str, SessionState] = {}

    def enrich(self, event: CanonicalMarketEvent) -> EnrichedMarketEvent:
        symbol = str(event.instrument_id)
        if symbol not in self.sessions:
            self.sessions[symbol] = SessionState()
            
        session = self.sessions[symbol]
        prev_close = session.close if session.close > 0 else event.price
        
        session.update(event.price, event.volume)
        
        hl2 = (session.high + session.low) / 2.0
        hlc3 = (session.high + session.low + session.close) / 3.0
        ohlc4 = (session.open + session.high + session.low + session.close) / 4.0
        
        tr1 = session.high - session.low
        tr2 = abs(session.high - prev_close)
        tr3 = abs(session.low - prev_close)
        true_range = max(tr1, tr2, tr3)
        
        gap_pct = ((session.open - prev_close) / prev_close) * 100.0 if prev_close > 0 else 0.0
        log_ret = math.log(event.price / prev_close) if prev_close > 0 and event.price > 0 else 0.0
        
        derived = DerivedMetrics(
            hl2=hl2, hlc3=hlc3, ohlc4=ohlc4, typical_price=hlc3,
            true_range=true_range, gap_percent=gap_pct, log_return=log_ret, session_volume=session.volume
        )
        
        return EnrichedMarketEvent(
            provenance=event.provenance, priority=event.priority, quality=event.quality,
            instrument_id=event.instrument_id, price=event.price, volume=event.volume,
            exchange_timestamp=event.exchange_timestamp, bid=event.bid, ask=event.ask, derived=derived
        )
