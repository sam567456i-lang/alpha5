import pytest
from datetime import datetime, timezone

from Backend.core.state import ExecutionContext, BaseState, StateLifecycle
from Backend.platforms.platform9_features.feature_framework import FeatureCompiler
from Backend.platforms.platform9_features.feature_registry import feature_registry

# Mock State for testing
class MockState(BaseState):
    def __init__(self, version=1):
        super().__init__(
            context=ExecutionContext("test", "test", "test", "test", "test", "test", "test", "test", "test", "test", 1, False, "1.0"),
            lifecycle=StateLifecycle.UPDATED,
            timestamp=datetime.now(timezone.utc),
            version=version,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
    @classmethod
    def calculate_next(cls, *args, **kwargs):
        pass
        
    def serialize(self):
        pass
        
    @classmethod
    def deserialize(cls, data):
        pass

# Ensure all modules are loaded to populate registry
import Backend.platforms.platform9_features.geometry_features
import Backend.platforms.platform9_features.price_action_features
import Backend.platforms.platform9_features.liquidity_features
import Backend.platforms.platform9_features.market_structure_features
import Backend.platforms.platform9_features.trend_features
import Backend.platforms.platform9_features.momentum_features
import Backend.platforms.platform9_features.volume_features
import Backend.platforms.platform9_features.volatility_features

@pytest.fixture
def compiler():
    context = ExecutionContext(
        session_id="test_session",
        trace_id="test_trace",
        correlation_id="test_corr",
        instrument_id="BTC-USD",
        environment="TEST",
        runtime_mode="BACKTEST",
        exchange="BINANCE",
        provider="BINANCE",
        market="CRYPTO",
        timezone="UTC",
        sequence_id=1,
        is_replay=False,
        build_version="1.0"
    )
    c = FeatureCompiler(context)
    c.load_plugins(feature_registry.list_features())
    return c

def test_feature_compiler_validation(compiler):
    """
    Test that if required states are missing, features aren't evaluated.
    """
    states = {}
    features = compiler.compile(states)
    assert len(features) == 0, "No features should be produced if required states are missing"

def test_feature_compiler_execution(compiler):
    """
    Test that features evaluate when their dependent states are present.
    """
    # Supply states for just one feature as an example: price_action.pinbar_rejection requires price_action.candlestick
    states = {
        "price_action.candlestick": MockState()
    }
    
    features = compiler.compile(states)
    
    assert "price_action.pinbar_rejection" in features
    feature = features["price_action.pinbar_rejection"]
    
    assert feature.value is True
    assert feature.feature_type.name == "Pinbar Rejection"
    assert "price_action.candlestick" in feature.source_states
