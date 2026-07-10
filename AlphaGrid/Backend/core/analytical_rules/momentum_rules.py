from typing import List, Optional
from Backend.core.interfaces.market_data import BarView
from Backend.core.interfaces.math_backend import MathBackend, NumericalPolicy, RollingState
from Backend.core.evidence_dtos.base import LineageRecord, PlatformIdentity
from Backend.core.evidence_dtos.momentum import (
    MomentumObject, MomentumPolicy, VelocityMeasurement, 
    AccelerationMeasurement, RateOfChangeMeasurement
)

class MomentumEngine:
    """
    O(1) Streaming Momentum Physics Engine.
    Exclusively consumes MarketDataView and delegates math to MathBackend.
    """
    def __init__(self, backend: MathBackend, policy: MomentumPolicy, rule_id: str = "RULE-MOM-001"):
        self.backend = backend
        self.policy = policy
        self.rule_id = rule_id
        self.num_policy = NumericalPolicy()
        
        # O(1) Rolling States for streaming derivations
        self.price_state = RollingState[float](window_size=policy.velocity_policy.lookback_window)
        self.velocity_state = RollingState[float](window_size=2) # Need prior velocity for acceleration

    def process_tick_stream(self, data_view: BarView) -> Optional[MomentumObject]:
        """
        Processes a single incoming bar update in O(1) amortized time.
        """
        current_bar = data_view.latest()
        if not current_bar:
            return None
            
        current_price = current_bar.close_price
        
        # Retrieve oldest BEFORE push to get N-periods ago
        was_full = self.price_state.is_full()
        oldest_price = self.price_state.get_oldest()
        self.price_state.push(current_price)
        
        if not was_full or oldest_price is None:
            return None # Not enough data for full lookback window
            
        # 1. Velocity (Current Price - Oldest Price)
        raw_velocity = current_price - oldest_price
        velocity = self.backend.apply_numerical_policy(raw_velocity, self.num_policy)
        
        # Push velocity to state for acceleration
        prev_velocity = self.velocity_state.get_newest()
        self.velocity_state.push(velocity)
        
        acceleration = 0.0
        if prev_velocity is not None:
            raw_accel = velocity - prev_velocity
            acceleration = self.backend.apply_numerical_policy(raw_accel, self.num_policy)
            
        # 2. Rate of Change
        safe_oldest_price = oldest_price
        if abs(safe_oldest_price) < self.num_policy.zero_threshold:
            safe_oldest_price = self.num_policy.epsilon # Protect against /0
            
        raw_roc = (current_price - safe_oldest_price) / safe_oldest_price
        roc = self.backend.apply_numerical_policy(raw_roc, self.num_policy)
        
        # 3. Construct Measurements
        vel_meas = VelocityMeasurement(absolute_velocity=velocity)
        accel_meas = AccelerationMeasurement(acceleration=acceleration)
        roc_meas = RateOfChangeMeasurement(roc_percentage=roc)
        
        # 4. Construct Object
        mo = MomentumObject(
            identity=PlatformIdentity(owner_family="Momentum", uuid=f"mom_{current_bar.temporal_context.event_time}"),
            lineage=self._build_lineage(current_bar.temporal_context.event_time),
            momentum_uuid=f"mom_{current_bar.temporal_context.event_time}",
            velocity=vel_meas,
            acceleration=accel_meas,
            rate_of_change=roc_meas
        )
        
        return mo

    def _build_lineage(self, timestamp: float) -> LineageRecord:
        return LineageRecord(
            platform="Platform10",
            family="Momentum",
            capability="PhysicsExtraction",
            source_dto_uuids=[],
            source_rule_ids=[self.rule_id],
            source_engine_id="MomentumEngine",
            parent_object_uuids=[],
            source_revision="1.0.0",
            version="1.0.0",
            replay_id="",
            timestamp=timestamp
        )
