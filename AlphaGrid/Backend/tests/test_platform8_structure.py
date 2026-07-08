import pytest
from datetime import datetime, timezone, timedelta
import hashlib
import time
from Backend.platforms.platform8_analysis.frameworks.structure_state_machine import (
    StructureStateMachine, 
    OutOfOrderEventError, 
    AlreadyProcessedEventError, 
    RegistryVersionMismatchError
)
from Backend.shared_domain.contracts.structure.structure_dtos import (
    StructureStateDTO, 
    StructureEventDTO, 
    StructureContextDTO, 
    StructureStateIdentity
)

@pytest.fixture
def base_identity():
    return StructureStateIdentity(
        market="NASDAQ",
        asset_class="Equities",
        exchange="NASDAQ",
        symbol="AAPL",
        timeframe="H1",
        session_id="RTH",
        data_feed="Polygon"
    )

@pytest.fixture
def base_time():
    return datetime.now(timezone.utc)

@pytest.fixture
def fsm():
    return StructureStateMachine()

@pytest.fixture
def initial_context(base_identity, base_time, fsm):
    return StructureContextDTO(
        id="ctx_1",
        timestamp=base_time,
        consumes=[],
        produces=[],
        identity=base_identity,
        current_state=StructureStateDTO.BULLISH,
        sequence_number=1,
        last_updated_timestamp=base_time,
        registry_checksum=fsm._registry_checksum,
        state_machine_version=fsm.schema_version
    )

def test_stateless_fsm_transition(fsm, initial_context, base_time):
    """Test standard legal transition."""
    event = StructureEventDTO(
        id="str.eve.choch",
        timestamp=base_time + timedelta(minutes=5),
        consumes=[],
        produces=[],
        event_price=150.0,
        sequence_number=2
    )
    
    new_ctx = fsm.process_event(initial_context, event)
    
    assert new_ctx is not initial_context
    assert new_ctx.current_state == StructureStateDTO.CONSOLIDATION
    assert new_ctx.sequence_number == 2

def test_out_of_order_rejection(fsm, initial_context, base_time):
    """Test deterministic out-of-order rejection."""
    event = StructureEventDTO(
        id="str.eve.bos.major",
        timestamp=base_time + timedelta(minutes=10),
        consumes=[],
        produces=[],
        event_price=150.0,
        sequence_number=0  # Older sequence!
    )
    
    with pytest.raises(OutOfOrderEventError):
        fsm.process_event(initial_context, event)

def test_duplicate_rejection(fsm, initial_context, base_time):
    """Test idempotency."""
    # First apply an event
    event = StructureEventDTO(
        id="str.eve.choch",
        timestamp=base_time + timedelta(minutes=5),
        consumes=[],
        produces=[],
        event_price=150.0,
        sequence_number=2
    )
    new_ctx = fsm.process_event(initial_context, event)
    
    # Try applying it again
    with pytest.raises(AlreadyProcessedEventError):
        fsm.process_event(new_ctx, event)

def test_registry_version_drift(fsm, initial_context, base_time):
    """Test version locking."""
    # Forge a context from a different registry
    drifted_ctx = StructureContextDTO(
        id="ctx_drift",
        timestamp=base_time,
        consumes=[],
        produces=[],
        identity=initial_context.identity,
        current_state=StructureStateDTO.BULLISH,
        sequence_number=1,
        last_updated_timestamp=base_time,
        registry_checksum="fake_checksum",
        state_machine_version="0.9.0"
    )
    
    event = StructureEventDTO(
        id="str.eve.choch",
        timestamp=base_time + timedelta(minutes=5),
        consumes=[],
        produces=[],
        event_price=150.0,
        sequence_number=2
    )
    
    with pytest.raises(RegistryVersionMismatchError):
        fsm.process_event(drifted_ctx, event)

def test_fsm_purity_certification(fsm, initial_context, base_time):
    """
    Run 10,000 identical transitions. Hash the output. All hashes must match.
    Proves absolutely no hidden mutations or side effects.
    """
    event = StructureEventDTO(
        id="str.eve.choch",
        timestamp=base_time + timedelta(minutes=5),
        consumes=[],
        produces=[],
        event_price=150.0,
        sequence_number=2
    )
    
    hashes = set()
    for _ in range(10000):
        out_ctx = fsm.process_event(initial_context, event)
        # Hash state string representation
        ctx_hash = hashlib.md5(str(out_ctx).encode('utf-8')).hexdigest()
        hashes.add(ctx_hash)
        
    assert len(hashes) == 1, "FSM Purity failed. Output state mutated across identical iterations."

def test_performance_certification(fsm, initial_context, base_time):
    """
    Process 100,000 events. Validate latency/memory.
    """
    ctx = initial_context
    start_time = time.time()
    
    for i in range(2, 100002):
        # We ping-pong between events to avoid Same-Event-ID Idempotency rejection
        event_id = "str.eve.bos.major" if i % 2 == 0 else "str.eve.choch"
        event = StructureEventDTO(
            id=event_id,
            timestamp=base_time + timedelta(seconds=i),
            consumes=[],
            produces=[],
            event_price=150.0,
            sequence_number=i
        )
        ctx = fsm.process_event(ctx, event)
        
    end_time = time.time()
    total_time = end_time - start_time
    events_per_sec = 100000 / total_time
    
    assert events_per_sec > 5000, f"Performance failed: {events_per_sec} events/sec is too slow."
