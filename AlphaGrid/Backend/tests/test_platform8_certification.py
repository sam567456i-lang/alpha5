import pytest
from datetime import datetime, timezone
from Backend.platforms.platform8_analysis.geometry_plugin import GeometryPlugin
from Backend.platforms.platform8_analysis.geometry_states import GeometryInputDTO
from Backend.platforms.platform8_analysis.price_action_plugin import PriceActionPlugin
from Backend.platforms.platform8_analysis.price_action_states import CandlestickInputDTO
from Backend.platforms.platform8_analysis.liquidity_plugin import LiquidityPlugin
from Backend.platforms.platform8_analysis.liquidity_states import LiquidityInputDTO
from Backend.platforms.platform8_analysis.market_structure_plugin import MarketStructurePlugin
from Backend.platforms.platform8_analysis.market_structure_states import MarketStructureInputDTO
from Backend.core.state import ExecutionContext

@pytest.fixture
def base_context():
    return ExecutionContext(
        session_id="test_session",
        trace_id="test_trace",
        correlation_id="test_correlation",
        instrument_id="TEST",
        environment="TEST",
        runtime_mode="TEST",
        exchange="TEST",
        provider="TEST",
        market="TEST",
        timezone="UTC",
        sequence_id=1,
        is_replay=False,
        build_version="1.0"
    )

class TestPlatform8Certification:
    
    def test_geometry_plugin_certification(self, base_context):
        plugin = GeometryPlugin()
        assert plugin.family_name == "Geometry"
        
        # 1. Unit Test
        inputs = {
            "geometry_input": GeometryInputDTO(
                timestamp=datetime.now(timezone.utc),
                price=102.0, high=105.0, low=95.0, volume=1000
            ),
            "previous_swing_state": None,
            "previous_extremes_state": None,
            "previous_range_state": None,
            "previous_sr_state": None,
            "previous_trendline_state": None,
            "previous_channel_state": None,
            "previous_compression_state": None,
        }
        
        output = plugin.execute(inputs, base_context)
        
        assert "ANA_PRICE_ACTION_SWING" in output
        assert "ANA_PRICE_ACTION_TIME_EXTREMES" in output
        
        swing_state = output["ANA_PRICE_ACTION_SWING"]
        
        # 2. State Lifecycle Test
        assert swing_state.context == base_context
        assert swing_state.version == 1
        assert swing_state.created_at is not None
        assert swing_state.updated_at is not None
        
        # 3. Snapshot Test
        serialized = swing_state.serialize()
        assert isinstance(serialized, dict)
        
        # 4. Incremental / Replay
        inputs["previous_swing_state"] = swing_state
        output2 = plugin.execute(inputs, base_context)
        
        assert "ANA_PRICE_ACTION_SWING" in output2
        assert output2["ANA_PRICE_ACTION_SWING"].version == 2

    def test_price_action_plugin_certification(self, base_context):
        plugin = PriceActionPlugin()
        inputs = {
            "candlestick_input": CandlestickInputDTO(
                timestamp=datetime.now(timezone.utc),
                open=100.0, high=105.0, low=95.0, close=102.0, volume=1000
            ),
            "previous_candle_state": None,
            "previous_engulfing_state": None,
            "previous_pinbar_state": None,
            "previous_inout_state": None,
            "previous_marudoji_state": None,
        }
        output = plugin.execute(inputs, base_context)
        state = output["ANA_PRICE_ACTION_CANDLESTICK"]
        assert state.version == 1
        assert state.context == base_context

    def test_liquidity_plugin_certification(self, base_context):
        plugin = LiquidityPlugin()
        inputs = {
            "liquidity_input": LiquidityInputDTO(
                timestamp=datetime.now(timezone.utc),
                price=100.0, high=105.0, low=95.0, volume=1000
            ),
            "previous_liquidity_state": None,
            "previous_sweep_state": None,
            "previous_hunt_state": None,
        }
        output = plugin.execute(inputs, base_context)
        state = output["ANA_MARKET_CONTEXT_LIQUIDITY_POOLS"]
        assert state.version == 1
        assert state.context == base_context

    def test_market_structure_plugin_certification(self, base_context):
        plugin = MarketStructurePlugin()
        inputs = {
            "market_structure_input": MarketStructureInputDTO(
                timestamp=datetime.now(timezone.utc),
                price=100.0, high=105.0, low=95.0, close=102.0
            ),
            "previous_bos_state": None,
            "previous_choch_state": None,
            "previous_mss_state": None,
            "previous_internal_external_state": None,
        }
        output = plugin.execute(inputs, base_context)
        state = output["ANA_MARKET_STRUCTURE_BOS"]
        assert state.version == 1
        assert state.context == base_context
