from typing import Type
import inspect
import os
import yaml
import json
from datetime import datetime, timezone, timedelta
from Backend.platforms.platform8_analysis.frameworks.detector_base import DetectorBase
from Backend.platforms.platform8_analysis.frameworks.structure_state_machine import (
    StructureStateMachine,
    OutOfOrderEventError,
    AlreadyProcessedEventError,
    InvalidStructureTransitionError
)
from Backend.shared_domain.contracts.structure.structure_dtos import (
    StructureStateDTO,
    StructureEventDTO,
    StructureContextDTO,
    StructureStateIdentity
)

class DetectorCertificationSuite:
    @staticmethod
    def certify(detector_class: Type[DetectorBase], capability_id: str, repo_root: str) -> bool:
        print(f"Starting certification for {detector_class.__name__} (Capability: {capability_id})...")
        
        if not issubclass(detector_class, DetectorBase):
            print(f"FAIL: {detector_class.__name__} does not inherit from DetectorBase.")
            return False
            
        if "structure" in detector_class.__name__.lower():
            if not DetectorCertificationSuite.certify_structure_state_machine():
                return False
                            
        print(f"PASS: {detector_class.__name__} successfully certified.")
        return True

    @staticmethod
    def certify_structure_state_machine() -> bool:
        print("Certifying Structure State Machine Transitions...")
        fsm = StructureStateMachine()
        
        base_time = datetime.now(timezone.utc)
        identity = StructureStateIdentity(
            market="NASDAQ",
            asset_class="Equities",
            exchange="NASDAQ",
            symbol="AAPL",
            timeframe="H1",
            session_id="RTH",
            data_feed="Polygon"
        )
        
        ctx = StructureContextDTO(
            id="ctx_1",
            timestamp=base_time,
            consumes=[],
            produces=[],
            identity=identity,
            current_state=StructureStateDTO.BULLISH,
            sequence_number=1,
            last_updated_timestamp=base_time
        )
        
        # 1. Valid Transition
        event_choch = StructureEventDTO(
            id="str.eve.choch",
            timestamp=base_time + timedelta(minutes=5),
            consumes=[],
            produces=[],
            event_price=100.0,
            sequence_number=2
        )
        try:
            next_ctx = fsm.process_event(ctx, event_choch)
            if next_ctx.current_state != StructureStateDTO.CONSOLIDATION:
                print("FAIL: CHOCH did not transition to CONSOLIDATION.")
                return False
        except Exception as e:
            print(f"FAIL: {e}")
            return False

        # 2. Out-of-Order Rejection (Sequence Number)
        event_past = StructureEventDTO(
            id="str.eve.bos",
            timestamp=base_time + timedelta(minutes=10), # Time is later
            consumes=[],
            produces=[],
            event_price=100.0,
            sequence_number=0 # Sequence is older
        )
        try:
            fsm.process_event(next_ctx, event_past)
            print("FAIL: Failed to reject out-of-order sequence.")
            return False
        except OutOfOrderEventError:
            pass

        # 3. Duplicate Idempotency Rejection
        event_dup = StructureEventDTO(
            id="str.eve.choch",
            timestamp=base_time + timedelta(minutes=5),
            consumes=[],
            produces=[],
            event_price=100.0,
            sequence_number=2
        )
        try:
            fsm.process_event(next_ctx, event_dup)
            print("FAIL: Failed to reject duplicate event.")
            return False
        except AlreadyProcessedEventError:
            pass
            
        # 4. Multi-Timeframe Identity Preservation
        if next_ctx.identity.timeframe != "H1":
            print("FAIL: MTF Isolation broken, lost timeframe context.")
            return False

        print("PASS: Structure State Machine advanced certification successful.")
        return True
