import pytest
from datetime import datetime
from Backend.market_intelligence.market_state_engine import MarketStateEngine, MarketState
from Backend.market_intelligence.session_engine import SessionEngine
from Backend.market_intelligence.trading_calendar import TradingCalendar
from Backend.market_intelligence.exchange_contract import NSEImplementation

def test_market_state_engine():
    exchange = NSEImplementation()
    session = SessionEngine(exchange)
    calendar = TradingCalendar(exchange)
    
    engine = MarketStateEngine(session_engine=session, trading_calendar=calendar)
    
    # 09:10 AM - Pre-open
    dt_preopen = datetime(2026, 7, 1, 9, 10, 0) # Wednesday
    assert engine.get_current_state(dt_preopen) == MarketState.PREOPEN
    
    # 10:00 AM - Open
    dt_open = datetime(2026, 7, 1, 10, 0, 0)
    assert engine.get_current_state(dt_open) == MarketState.OPEN
    
    # 03:45 PM - Post-market
    dt_post = datetime(2026, 7, 1, 15, 45, 0)
    assert engine.get_current_state(dt_post) == MarketState.POSTMARKET
    
    # 06:00 PM - Closed
    dt_closed = datetime(2026, 7, 1, 18, 0, 0)
    assert engine.get_current_state(dt_closed) == MarketState.CLOSED
    
    # Saturday - Holiday
    dt_sat = datetime(2026, 7, 4, 10, 0, 0) # Saturday
    assert engine.get_current_state(dt_sat) == MarketState.HOLIDAY
    
    # Manual Override
    engine.set_manual_override(MarketState.CIRCUIT)
    assert engine.get_current_state(dt_open) == MarketState.CIRCUIT
