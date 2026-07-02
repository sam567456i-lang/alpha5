"""Unit tests for the Shared Models module."""

from datetime import datetime, timezone
from decimal import Decimal
import os
import unittest
from uuid import uuid4

from pydantic import ValidationError

from Shared.enums import (
    NotificationSeverity,
    RecommendationStatus,
    ResearchStatus,
    TradeDirection,
    TradeStatus,
)
from Shared.models import (
    Evidence,
    MarketSnapshot,
    Opportunity,
    Portfolio,
    Position,
    Recommendation,
    Trade,
)
from Shared.dto import (
    CreateTradeRequest,
    ErrorInfo,
    ErrorResponse,
    LoginRequest,
)


class SharedEnumsTests(unittest.TestCase):
    def test_enum_values(self) -> None:
        self.assertEqual(RecommendationStatus.NEW, "NEW")
        self.assertEqual(TradeDirection.BUY, "BUY")
        self.assertEqual(TradeStatus.PENDING, "PENDING")
        self.assertEqual(ResearchStatus.DRAFT, "DRAFT")
        self.assertEqual(NotificationSeverity.INFO, "INFO")


class SharedModelsTests(unittest.TestCase):
    def test_market_snapshot_valid(self) -> None:
        snapshot = MarketSnapshot(
            symbol="NIFTY",
            exchange="NSE",
            instrument_type="OPT",
            last_price=Decimal("24000.50"),
            open=Decimal("23900.00"),
            high=Decimal("24100.00"),
            low=Decimal("23850.00"),
            close=Decimal("23950.00"),
            volume=150000,
            bid=Decimal("24000.00"),
            ask=Decimal("24001.00"),
            timestamp=datetime.now(tz=timezone.utc),
        )
        self.assertEqual(snapshot.symbol, "NIFTY")
        self.assertEqual(snapshot.volume, 150000)

    def test_market_snapshot_negative_prices_fail(self) -> None:
        with self.assertRaises(ValidationError):
            MarketSnapshot(
                symbol="NIFTY",
                exchange="NSE",
                instrument_type="OPT",
                last_price=Decimal("-1.0"),
                open=Decimal("23900.00"),
                high=Decimal("24100.00"),
                low=Decimal("23850.00"),
                close=Decimal("23950.00"),
                volume=100,
                timestamp=datetime.now(tz=timezone.utc),
            )

    def test_market_snapshot_negative_volume_fails(self) -> None:
        with self.assertRaises(ValidationError):
            MarketSnapshot(
                symbol="NIFTY",
                exchange="NSE",
                instrument_type="OPT",
                last_price=Decimal("24000.00"),
                open=Decimal("23900.00"),
                high=Decimal("24100.00"),
                low=Decimal("23850.00"),
                close=Decimal("23950.00"),
                volume=-1,
                timestamp=datetime.now(tz=timezone.utc),
            )

    def test_market_snapshot_naive_timestamp_fails(self) -> None:
        with self.assertRaises(ValidationError):
            MarketSnapshot(
                symbol="NIFTY",
                exchange="NSE",
                instrument_type="OPT",
                last_price=Decimal("24000.00"),
                open=Decimal("23900.00"),
                high=Decimal("24100.00"),
                low=Decimal("23850.00"),
                close=Decimal("23950.00"),
                volume=100,
                timestamp=datetime.now(),  # naive
            )

    def test_evidence_invalid_confidence_fails(self) -> None:
        with self.assertRaises(ValidationError):
            Evidence(
                evidence_id=uuid4(),
                version=1,
                source="rsi_indicator",
                category="technical",
                instrument="NIFTY",
                timeframe="15m",
                confidence=Decimal("1.2"),  # > 1.0
                weight=Decimal("0.5"),
                score=Decimal("0.8"),
                explanation="RSI oversold",
                timestamp=datetime.now(tz=timezone.utc),
            )

    def test_opportunity_negative_score_fails(self) -> None:
        with self.assertRaises(ValidationError):
            Opportunity(
                opportunity_id=uuid4(),
                symbol="NIFTY",
                strategy="breakout",
                direction=TradeDirection.BUY,
                opportunity_score=Decimal("-0.5"),
                created_at=datetime.now(tz=timezone.utc),
                status="NEW",
            )

    def test_recommendation_nested_evidence_valid(self) -> None:
        evidence_item = Evidence(
            evidence_id=uuid4(),
            version=1,
            source="rsi_indicator",
            category="technical",
            instrument="NIFTY",
            timeframe="15m",
            confidence=Decimal("0.8"),
            weight=Decimal("0.5"),
            score=Decimal("0.8"),
            explanation="RSI oversold",
            timestamp=datetime.now(tz=timezone.utc),
        )
        rec = Recommendation(
            recommendation_id=uuid4(),
            opportunity_id=uuid4(),
            symbol="NIFTY",
            strategy="breakout",
            direction=TradeDirection.BUY,
            entry_price=Decimal("24000.00"),
            stop_loss=Decimal("23800.00"),
            targets=[Decimal("24200.00"), Decimal("24400.00")],
            confidence=Decimal("0.85"),
            opportunity_score=Decimal("9.0"),
            status=RecommendationStatus.NEW,
            timestamp=datetime.now(tz=timezone.utc),
            evidence=[evidence_item],
        )
        self.assertEqual(len(rec.evidence), 1)
        self.assertEqual(rec.evidence[0].source, "rsi_indicator")

    def test_portfolio_negative_capital_fails(self) -> None:
        with self.assertRaises(ValidationError):
            Portfolio(
                portfolio_id=uuid4(),
                name="Aggressive",
                capital=Decimal("-100.0"),
                invested_amount=Decimal("0.0"),
                unrealized_pnl=Decimal("0.0"),
                realized_pnl=Decimal("0.0"),
                created_at=datetime.now(tz=timezone.utc),
            )

    def test_position_zero_quantity_fails(self) -> None:
        with self.assertRaises(ValidationError):
            Position(
                position_id=uuid4(),
                portfolio_id=uuid4(),
                symbol="NIFTY",
                quantity=0,
                average_price=Decimal("100.0"),
                current_price=Decimal("100.0"),
                unrealized_pnl=Decimal("0.0"),
            )

    def test_trade_zero_quantity_fails(self) -> None:
        with self.assertRaises(ValidationError):
            Trade(
                trade_id=uuid4(),
                portfolio_id=uuid4(),
                symbol="NIFTY",
                trade_type=TradeDirection.BUY,
                quantity=0,
                entry_price=Decimal("100.0"),
                execution_time=datetime.now(tz=timezone.utc),
                status=TradeStatus.PENDING,
            )


class SharedDTOTests(unittest.TestCase):
    def test_login_request_validation(self) -> None:
        req = LoginRequest(username="admin", password="password123")
        self.assertEqual(req.username, "admin")

        with self.assertRaises(ValidationError):
            LoginRequest(username="", password="password123")

    def test_create_trade_request_json_round_trip(self) -> None:
        req = CreateTradeRequest(
            portfolio_id=uuid4(),
            symbol="NIFTY",
            trade_type=TradeDirection.SELL,
            quantity=10,
            entry_price=Decimal("24000.00"),
        )
        serialized = req.model_dump_json()
        deserialized = CreateTradeRequest.model_validate_json(serialized)
        self.assertEqual(deserialized.symbol, "NIFTY")
        self.assertEqual(deserialized.quantity, 10)
        self.assertEqual(deserialized.trade_type, TradeDirection.SELL)

    def test_error_response_nesting(self) -> None:
        err_info = ErrorInfo(
            code="INVALID_FUNDS",
            message="Insufficient capital to execute trade.",
            details=["Requires 200000, balance is 50000"],
        )
        response = ErrorResponse(success=False, error=err_info)
        self.assertFalse(response.success)
        self.assertEqual(response.error.code, "INVALID_FUNDS")


class TypeScriptGenerationTest(unittest.TestCase):
    def test_generated_file_exists_and_contains_types(self) -> None:
        path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "../../Shared/generated/interfaces.ts",
            )
        )
        self.assertTrue(os.path.exists(path), f"File not found: {path}")
        with open(path, "r", encoding="utf-8") as handle:
            content = handle.read()

        self.assertIn("export enum RecommendationStatus", content)
        self.assertIn("export interface MarketSnapshot", content)
        self.assertIn("export interface Recommendation", content)
        self.assertIn("export interface StandardResponse", content)
