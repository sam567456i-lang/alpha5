"""Unit and integration tests for the AlphaGrid API layer."""

from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from Backend.api.app import create_app
from Backend.foundation.dependency_injection_container import DependencyContainer
from Backend.market_intelligence.session_engine import SessionEngine
from Backend.market_intelligence.universe_manager import UniverseManager
from Backend.market_intelligence.normalization_engine import NormalizationEngine
from Backend.market_intelligence.providers.abstract_market_data_provider import HistoricalDataProvider
from Backend.market_intelligence.historical_market_pipeline import HistoricalMarketPipeline

# ---------------------------------------------------------------------------
# Test client setup
# ---------------------------------------------------------------------------

container = DependencyContainer()
container.register_instance("session_engine", SessionEngine())
container.register_instance("universe_manager", UniverseManager())
container.register_instance("normalization_engine", NormalizationEngine())
container.register_instance("historical_market_pipeline", HistoricalMarketPipeline(None, None, None, None))

app = create_app(container=container, debug=True)
client = TestClient(app, raise_server_exceptions=False)


class ResponseEnvelopeTests(unittest.TestCase):
    """Verify that every success response contains the standard envelope keys."""

    def _assert_success_envelope(self, response_json: dict) -> None:
        self.assertIn("success", response_json)
        self.assertIn("data", response_json)
        self.assertIn("message", response_json)
        self.assertIn("timestamp", response_json)
        self.assertIn("execution_time", response_json)
        self.assertTrue(response_json["success"])

    def test_system_status_envelope(self) -> None:
        r = client.get("/api/v1/system/status")
        self.assertEqual(r.status_code, 200)
        self._assert_success_envelope(r.json())

    def test_dashboard_envelope(self) -> None:
        r = client.get("/api/v1/dashboard")
        self.assertEqual(r.status_code, 200)
        self._assert_success_envelope(r.json())

    def test_market_status_envelope(self) -> None:
        r = client.get("/api/v1/market/status")
        self.assertEqual(r.status_code, 200)
        self._assert_success_envelope(r.json())

    def test_recommendations_live_envelope(self) -> None:
        r = client.get("/api/v1/recommendations/live")
        self.assertEqual(r.status_code, 200)
        self._assert_success_envelope(r.json())

    def test_ai_models_envelope(self) -> None:
        r = client.get("/api/v1/ai/models")
        self.assertEqual(r.status_code, 200)
        self._assert_success_envelope(r.json())


class ErrorHandlingTests(unittest.TestCase):
    """Verify that error responses follow the standard error envelope."""

    def _assert_error_envelope(self, response_json: dict) -> None:
        self.assertIn("success", response_json)
        self.assertIn("error_code", response_json)
        self.assertIn("message", response_json)
        self.assertFalse(response_json["success"])

    def test_not_found_recommendation(self) -> None:
        r = client.get("/api/v1/recommendations/00000000-0000-0000-0000-000000000000")
        self.assertEqual(r.status_code, 404)
        body = r.json()
        self._assert_error_envelope(body)
        self.assertEqual(body["error_code"], "NOT_FOUND")

    def test_not_found_strategy(self) -> None:
        r = client.get("/api/v1/strategies/00000000-0000-0000-0000-000000000000")
        self.assertEqual(r.status_code, 404)
        body = r.json()
        self._assert_error_envelope(body)
        self.assertEqual(body["error_code"], "NOT_FOUND")

    def test_not_found_report(self) -> None:
        r = client.get("/api/v1/reports/00000000-0000-0000-0000-000000000000")
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r.json()["error_code"], "NOT_FOUND")

    def test_invalid_uuid_returns_422(self) -> None:
        r = client.get("/api/v1/strategies/not-a-uuid")
        # FastAPI returns 422 for path parameter validation failures
        self.assertIn(r.status_code, [400, 422])

    def test_unknown_route_returns_404(self) -> None:
        r = client.get("/api/v1/nonexistent-endpoint")
        self.assertEqual(r.status_code, 404)


class MarketRouterTests(unittest.TestCase):
    def test_market_status(self) -> None:
        r = client.get("/api/v1/market/status")
        self.assertEqual(r.status_code, 200)
        data = r.json()["data"]
        self.assertIn("is_open", data)
        self.assertIn("session", data)
        self.assertIn("exchange", data)

    def test_market_breadth(self) -> None:
        r = client.get("/api/v1/market/breadth")
        self.assertEqual(r.status_code, 200)
        data = r.json()["data"]
        self.assertIn("advances", data)
        self.assertIn("declines", data)

    def test_market_regime(self) -> None:
        r = client.get("/api/v1/market/regime")
        self.assertEqual(r.status_code, 200)
        data = r.json()["data"]
        self.assertIn("regime", data)
        self.assertIn("confidence", data)

    def test_market_instruments_with_filter(self) -> None:
        r = client.get("/api/v1/market/instruments?exchange=NSE")
        self.assertEqual(r.status_code, 200)

    def test_market_ohlcv_requires_symbol(self) -> None:
        r = client.get("/api/v1/market/ohlcv")
        self.assertIn(r.status_code, [400, 422])

    def test_market_news(self) -> None:
        r = client.get("/api/v1/market/news?limit=5")
        self.assertEqual(r.status_code, 200)

    def test_market_calendar(self) -> None:
        r = client.get("/api/v1/market/calendar")
        self.assertEqual(r.status_code, 200)


class OptionsRouterTests(unittest.TestCase):
    def test_option_chain_requires_symbol(self) -> None:
        r = client.get("/api/v1/options/chain")
        self.assertIn(r.status_code, [400, 422])

    def test_option_chain_with_symbol(self) -> None:
        r = client.get("/api/v1/options/chain?symbol=NIFTY")
        self.assertEqual(r.status_code, 200)

    def test_pcr_with_symbol(self) -> None:
        r = client.get("/api/v1/options/pcr?symbol=NIFTY")
        self.assertEqual(r.status_code, 200)
        data = r.json()["data"]
        self.assertIn("pcr", data)


class PortfolioRouterTests(unittest.TestCase):
    def test_get_portfolio(self) -> None:
        r = client.get("/api/v1/portfolio")
        self.assertEqual(r.status_code, 200)
        data = r.json()["data"]
        self.assertIn("capital", data)
        self.assertIn("positions", data)

    def test_add_trade_valid(self) -> None:
        r = client.post(
            "/api/v1/portfolio/trades",
            json={
                "symbol": "NIFTY",
                "trade_type": "BUY",
                "quantity": 50,
                "entry_price": 24000.0,
            },
        )
        self.assertEqual(r.status_code, 201)

    def test_add_trade_invalid_quantity(self) -> None:
        r = client.post(
            "/api/v1/portfolio/trades",
            json={
                "symbol": "NIFTY",
                "trade_type": "BUY",
                "quantity": -1,
                "entry_price": 24000.0,
            },
        )
        self.assertIn(r.status_code, [400, 422])

    def test_add_trade_missing_symbol(self) -> None:
        r = client.post(
            "/api/v1/portfolio/trades",
            json={"trade_type": "BUY", "quantity": 10, "entry_price": 100.0},
        )
        self.assertIn(r.status_code, [400, 422])

    def test_update_nonexistent_trade(self) -> None:
        r = client.put(
            "/api/v1/portfolio/trades/00000000-0000-0000-0000-000000000000",
            json={"exit_price": 24500.0},
        )
        self.assertEqual(r.status_code, 404)

    def test_archive_nonexistent_trade(self) -> None:
        r = client.delete("/api/v1/portfolio/trades/00000000-0000-0000-0000-000000000000")
        self.assertEqual(r.status_code, 404)


class RecommendationsRouterTests(unittest.TestCase):
    def test_get_live_recommendations(self) -> None:
        r = client.get("/api/v1/recommendations/live")
        self.assertEqual(r.status_code, 200)

    def test_get_history_paginated(self) -> None:
        r = client.get("/api/v1/recommendations/history?page=1&page_size=10")
        self.assertEqual(r.status_code, 200)
        body = r.json()
        self.assertIn("pagination", body)
        self.assertIn("total", body["pagination"])

    def test_get_history_invalid_page_size(self) -> None:
        r = client.get("/api/v1/recommendations/history?page_size=999")
        self.assertIn(r.status_code, [400, 422])


class SystemRouterTests(unittest.TestCase):
    def test_system_status(self) -> None:
        r = client.get("/api/v1/system/status")
        self.assertEqual(r.status_code, 200)
        data = r.json()["data"]
        self.assertIn("status", data)
        self.assertIn("components", data)
        self.assertIn("live_mode", data)

    def test_start_live(self) -> None:
        r = client.post("/api/v1/system/live/start")
        self.assertIn(r.status_code, [200, 201])

    def test_stop_live(self) -> None:
        r = client.post("/api/v1/system/live/stop")
        self.assertEqual(r.status_code, 200)

    def test_pause_live(self) -> None:
        r = client.post("/api/v1/system/live/pause")
        self.assertEqual(r.status_code, 200)

    def test_resume_live(self) -> None:
        r = client.post("/api/v1/system/live/resume")
        self.assertEqual(r.status_code, 200)


class DashboardRouterTests(unittest.TestCase):
    def test_get_dashboard(self) -> None:
        r = client.get("/api/v1/dashboard")
        self.assertEqual(r.status_code, 200)
        data = r.json()["data"]
        self.assertIn("market_regime", data)
        self.assertIn("opportunity_count", data)

    def test_get_layout(self) -> None:
        r = client.get("/api/v1/dashboard/layout")
        self.assertEqual(r.status_code, 200)
        data = r.json()["data"]
        self.assertIn("widgets", data)

    def test_save_layout(self) -> None:
        r = client.put("/api/v1/dashboard/layout", json={"widgets": [], "version": 1})
        self.assertEqual(r.status_code, 200)


class ResearchRouterTests(unittest.TestCase):
    def test_list_experiments(self) -> None:
        r = client.get("/api/v1/research")
        self.assertEqual(r.status_code, 200)
        self.assertIn("pagination", r.json())

    def test_run_backtest(self) -> None:
        from Backend.research.strategies.registry import StrategyRegistry
        from Backend.research.strategies.definition import StrategyDefinition
        from Backend.methodology.base import AbstractMethodology
        from Backend.methodology.evaluation import MethodologyEvaluation
        from datetime import datetime, timezone

        class DummyMethodology(AbstractMethodology):
            def __init__(self): pass
            @classmethod
            def get_name(cls): return "Dummy"
            def evaluate(self, ctx): return MethodologyEvaluation("Dummy", datetime.now(timezone.utc), True, 1, 1.0)

        from Backend.research.engine.strategy_interface import AbstractStrategy
        
        class MockApiStrategy(AbstractStrategy):
            def __init__(self, parameters: dict, random_generator: Any, **kwargs):
                super().__init__(parameters, random_generator)
            def on_market_event(self, event): pass
            
        StrategyRegistry._definitions["BREAKOUT_V1"] = StrategyDefinition(
            id="BREAKOUT_V1",
            strategy_class=MockApiStrategy,
            methodology=DummyMethodology,
            features=[], concepts=[], primitive_signals=[], parameters={}
        )
        from Backend.research.engine.strategy_interface import STRATEGY_REGISTRY
        if "BREAKOUT_V1" not in STRATEGY_REGISTRY._registry:
            STRATEGY_REGISTRY.register("BREAKOUT_V1", MockApiStrategy)
        r = client.post(
            "/api/v1/research/backtest",
            json={
                "strategy": "BREAKOUT_V1",
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
            },
        )
        self.assertEqual(r.status_code, 201)

    def test_start_replay(self) -> None:
        r = client.post(
            "/api/v1/research/replay",
            json={"symbol": "NIFTY", "date": "2024-06-01"},
        )
        self.assertEqual(r.status_code, 201)


class ReportsRouterTests(unittest.TestCase):
    def test_list_reports(self) -> None:
        r = client.get("/api/v1/reports")
        self.assertEqual(r.status_code, 200)

    def test_generate_report(self) -> None:
        r = client.post(
            "/api/v1/reports/generate",
            json={"report_type": "daily_market"},
        )
        self.assertEqual(r.status_code, 201)


class WebSocketHubTests(unittest.TestCase):
    """Unit tests for ConnectionHub logic (no real WebSocket needed)."""

    def test_hub_initial_state(self) -> None:
        from Backend.api.websocket.hub import Channel, ConnectionHub

        test_hub = ConnectionHub()
        for channel in Channel:
            self.assertEqual(test_hub.connection_count(channel), 0)

    def test_channel_enum_values(self) -> None:
        from Backend.api.websocket.hub import Channel

        self.assertEqual(Channel.MARKET, "market")
        self.assertEqual(Channel.RECOMMENDATIONS, "recommendations")
        self.assertEqual(Channel.PORTFOLIO, "portfolio")
        self.assertEqual(Channel.AI, "ai")
        self.assertEqual(Channel.NEWS, "news")
        self.assertEqual(Channel.SYSTEM, "system")
