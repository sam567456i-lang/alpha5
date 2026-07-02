"""Tests for Scientific Evaluation Subsystem."""

import pytest
import numpy as np
from Backend.research.evaluation.report import ScientificEvaluationReport
from Backend.research.evaluation.metrics import MetricsCalculator
from Backend.research.evaluation.policy import PromotionPolicy
from Backend.research.evaluation.evaluator import ScientificEvaluator
from Backend.research.evaluation.promotion import PromotionEngine
from Backend.research.evaluation.registry import EvaluationRegistry
from Backend.research.experiments.registry import ResearchRegistry
from Shared.enums.experiment_status import ExperimentStatus

def test_profitability_metrics_known_vectors():
    trades = [
        {"pnl": 100.0},
        {"pnl": -50.0},
        {"pnl": 150.0},
        {"pnl": -100.0},
        {"pnl": 50.0}
    ]
    # Wins: 100, 150, 50 -> Gross = 300
    # Losses: -50, -100 -> Gross = 150
    # Total Trades = 5, Wins = 3 (60% WR)
    # Avg Win = 100, Avg Loss = 75
    # Profit Factor = 300 / 150 = 2.0
    # Payoff Ratio = 100 / 75 = 1.333
    # Expectancy = (0.6 * 100) - (0.4 * 75) = 60 - 30 = 30
    
    metrics = MetricsCalculator.calculate_profitability(trades, initial_capital=1000.0)
    
    assert metrics.win_rate == 0.6
    assert metrics.profit_factor == 2.0
    assert pytest.approx(metrics.payoff_ratio, 0.01) == 1.33
    assert metrics.expectancy == 30.0
    assert metrics.total_return == 0.15 # 150 / 1000

def test_risk_metrics_known_vectors():
    # Equity curve
    curve = [100.0, 110.0, 90.0, 105.0, 120.0]
    # Max DD: 
    # Maxes: [100, 110, 110, 110, 120]
    # Drawdowns: [0, 0, (90-110)/110 = -18.18%, (105-110)/110 = -4.54%, 0]
    # Max DD = 18.18%
    
    metrics = MetricsCalculator.calculate_risk(curve, risk_free_rate=0.0)
    
    assert pytest.approx(metrics.max_drawdown, 0.01) == 0.1818
    # Annualized Return Approx = (120/100) - 1 = 0.20
    # Calmar = 0.20 / 0.1818 = 1.1
    assert pytest.approx(metrics.calmar_ratio, 0.1) == 1.1

def test_edge_cases_empty_and_single_trade():
    empty_prof = MetricsCalculator.calculate_profitability([])
    assert empty_prof.win_rate == 0.0
    
    single_prof = MetricsCalculator.calculate_profitability([{"pnl": 100.0}])
    assert single_prof.win_rate == 1.0
    assert single_prof.profit_factor == 999.0 # Infinity representation

def test_edge_cases_zero_volatility():
    curve = [100.0, 100.0, 100.0, 100.0]
    risk = MetricsCalculator.calculate_risk(curve)
    assert risk.sharpe_ratio == 0.0
    assert risk.sortino_ratio == 0.0
    assert risk.max_drawdown == 0.0

def test_promotion_policy():
    policy = PromotionPolicy(min_trades=10, min_sharpe=1.0)
    
    # Passing Report
    evaluator = ScientificEvaluator(policy=policy)
    
    # Create variance to get a non-zero t-stat
    pnls = [10.0, 12.0, 8.0, 15.0, 5.0] * 3
    trades_pass = [{"pnl": p} for p in pnls]
    
    report = evaluator.evaluate(
        experiment_id="EXP_1", 
        hypothesis_id="RH_1",
        trades=trades_pass,
        equity_curve=[100.0 + i*10 for i in range(16)] # Constant growth, high sharpe
    )
    
    assert report.is_promoted is True
    assert len(report.failure_reasons) == 0
    
    # Failing Report (too few trades)
    report_fail = evaluator.evaluate(
        experiment_id="EXP_2", 
        hypothesis_id="RH_1",
        trades=[{"pnl": 10.0}] * 5,
        equity_curve=[100.0, 110.0, 120.0, 130.0, 140.0, 150.0]
    )
    
    assert report_fail.is_promoted is False
    assert any("Insufficient trades" in r for r in report_fail.failure_reasons)

def test_promotion_engine_routing():
    EvaluationRegistry.clear()
    research_registry = ResearchRegistry()
    engine = PromotionEngine(research_registry=research_registry)
    
    evaluator = ScientificEvaluator(policy=PromotionPolicy(min_trades=5))
    
    pnls_pass = [10.0, 12.0, 8.0, 15.0, 5.0] * 2
    trades_pass = [{"pnl": p} for p in pnls_pass]
    
    # Promoted
    report_pass = evaluator.evaluate(
        experiment_id="EXP_PASS", hypothesis_id="RH_1",
        trades=trades_pass,
        equity_curve=[100.0 + i*10 for i in range(11)]
    )
    engine.process(report_pass)
    
    # Rejected
    report_fail = evaluator.evaluate(
        experiment_id="EXP_FAIL", hypothesis_id="RH_1",
        trades=[{"pnl": -10.0}] * 10,
        equity_curve=[100.0 - i*10 for i in range(11)]
    )
    engine.process(report_fail)
    
    # Both should be in Evaluation Registry
    assert len(EvaluationRegistry.get_all()) == 2
    
    # Only EXP_PASS should be marked COMPLETED in ResearchRegistry
    exp_pass_data = research_registry.get_record("EXP_PASS")
    assert exp_pass_data["status"] == ExperimentStatus.COMPLETED.value
    
    # EXP_FAIL should NOT be in ResearchRegistry
    assert research_registry.get_record("EXP_FAIL") == {}
