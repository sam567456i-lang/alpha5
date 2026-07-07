import pytest
from datetime import datetime, timezone
from Backend.core.state import StateLifecycle
from Backend.core.events import CanonicalMarketEvent, EventProvenance
from Backend.dtos.instrument import InstrumentID, AssetClass
from Backend.market_foundation.states import SessionState, TimeState, CalendarState

def _create_event(price: float, volume: float, dt: datetime) -> CanonicalMarketEvent:
    provenance = EventProvenance(
        trace_id="t1", event_id="e1", parent_event_id=None,
        origin_service="test", origin_provider="test", schema_version=1
    )
    instrument_id = InstrumentID("NIFTY", "NSE", AssetClass.EQUITY)
    return CanonicalMarketEvent(
        provenance=provenance,
        instrument_id=instrument_id,
        price=price,
        volume=volume,
        exchange_timestamp=dt
    )

def test_session_state_incremental():
    dt1 = datetime(2023, 10, 5, 9, 15, tzinfo=timezone.utc)
    ev1 = _create_event(20000.0, 100, dt1)
    
    # Tick 1: New session
    s1 = SessionState.calculate_next(None, ev1)
    assert s1.lifecycle == StateLifecycle.CREATED
    assert s1.session_open == 20000.0
    assert s1.session_high == 20000.0
    assert s1.session_low == 20000.0
    assert s1.session_volume == 100.0
    assert s1.version == 1

    # Tick 2: Update session
    dt2 = datetime(2023, 10, 5, 9, 16, tzinfo=timezone.utc)
    ev2 = _create_event(20100.0, 50, dt2)
    s2 = SessionState.calculate_next(s1, ev2)
    assert s2.lifecycle == StateLifecycle.UPDATED
    assert s2.session_high == 20100.0
    assert s2.session_low == 20000.0
    assert s2.session_volume == 150.0
    assert s2.version == 2
    
    # Tick 3: New Day
    dt3 = datetime(2023, 10, 6, 9, 15, tzinfo=timezone.utc)
    ev3 = _create_event(19900.0, 200, dt3)
    s3 = SessionState.calculate_next(s2, ev3)
    assert s3.lifecycle == StateLifecycle.CREATED
    assert s3.session_open == 19900.0
    assert s3.session_volume == 200.0
    assert s3.version == 1

def test_time_state():
    dt_pre = datetime(2023, 10, 5, 9, 10, tzinfo=timezone.utc)
    ev_pre = _create_event(20000.0, 100, dt_pre)
    t1 = TimeState.calculate_next(None, ev_pre)
    assert t1.is_premarket == True
    assert t1.is_regular_hours == False
    
    dt_reg = datetime(2023, 10, 5, 10, 15, tzinfo=timezone.utc)
    ev_reg = _create_event(20000.0, 100, dt_reg)
    t2 = TimeState.calculate_next(t1, ev_reg)
    assert t2.is_premarket == False
    assert t2.is_regular_hours == True
    assert t2.minutes_since_open == 60
    assert t2.minutes_to_close == 315

def test_calendar_state():
    dt = datetime(2023, 10, 5, 9, 15, tzinfo=timezone.utc) # 2023-10-05 is a Thursday
    ev = _create_event(20000.0, 100, dt)
    s1 = SessionState.calculate_next(None, ev)
    
    c1 = CalendarState.calculate_next(None, s1)
    assert c1.day_of_week == 3 # Thursday is 3
    assert c1.is_expiry_day == True

def test_state_serialization():
    dt = datetime(2023, 10, 5, 9, 15, tzinfo=timezone.utc)
    ev = _create_event(20000.0, 100, dt)
    s1 = SessionState.calculate_next(None, ev)
    
    data = s1.serialize()
    assert data["lifecycle"] == "CREATED"
    
    s2 = SessionState.deserialize(data)
    assert s2.session_open == 20000.0
    assert s2.lifecycle == StateLifecycle.CREATED
    assert s2.version == 1
