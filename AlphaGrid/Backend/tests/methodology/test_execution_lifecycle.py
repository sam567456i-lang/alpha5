import pytest
from Backend.core.methodology.narrative_node import TradeSetupNode, MarketContextNode
from Backend.core.methodology.narrative_types import NarrativeNodeType, NarrativeStage
from Backend.core.methodology.scoring_engine import ScoringEngine, MethodologyScorePolicy
from Backend.core.methodology.decision_engine import DecisionEngine
from Backend.core.methodology.execution_planner import ExecutionPlanner
from Backend.core.methodology.position_lifecycle import PositionLifecycleEngine
from Backend.core.methodology.portfolio_state import PortfolioState
from Backend.core.methodology.risk_engine import RiskEngine
from Backend.core.methodology.conflict_engine import ConflictEngine

def test_execution_lifecycle():
    # 1. Setup
    setup = TradeSetupNode(node_id="setup_1", concept_name="Bullish Setup", concept_type=NarrativeNodeType.SETUP, stage=NarrativeStage.SETUP)
    
    # 2. Scoring
    def extract_trend_alignment(setup_node): return True
    def extract_time_alignment(setup_node): return True
    
    engine = ScoringEngine({"trend": extract_trend_alignment, "time": extract_time_alignment})
    fv = engine.extract_features(setup)
    
    policy = MethodologyScorePolicy(methodology_name="TEST", weights={"trend": 50, "time": 50})
    score_res = engine.score_setup(fv, policy)
    
    assert score_res.score == 100
    assert score_res.grade == "A"
    
    # 3. Decision
    decision_engine = DecisionEngine(min_score_to_execute=80.0)
    decision = decision_engine.evaluate(setup, score_res)
    
    assert decision.decision == "EXECUTE"
    
    # 4. Planning
    planner = ExecutionPlanner(default_risk_pct=1.0)
    plan = planner.plan(decision, entry_price=100.0, stop_price=95.0, target_price=110.0)
    
    assert plan is not None
    assert plan.position_size == 1.0
    
    # 5. Position Management
    lifecycle = PositionLifecycleEngine()
    pos = lifecycle.open_position(plan)
    
    assert pos.status == "OPEN"
    assert pos.average_entry_price == 100.0
    
    mgmt = lifecycle.manage_position(pos, "MOVE_STOP", "Stop to BE")
    assert mgmt.action_type == "MOVE_STOP"
    
    exit_node = lifecycle.close_position(pos, "TARGET_HIT", 10.0)
    assert exit_node.exit_reason == "TARGET_HIT"

def test_risk_engine():
    state = PortfolioState(daily_realized_pnl_pct=-3.5, max_daily_risk_pct=3.0)
    engine = RiskEngine()
    narrative = engine.evaluate(state)
    
    assert narrative is not None
    assert narrative.risk_level == "CRITICAL"

def test_conflict_engine():
    bullish = MarketContextNode(node_id="ctx_1", concept_name="Bullish Context", concept_type=NarrativeNodeType.MARKET_CONTEXT, stage=NarrativeStage.CONTEXT)
    bearish = MarketContextNode(node_id="ctx_2", concept_name="Bearish Context", concept_type=NarrativeNodeType.MARKET_CONTEXT, stage=NarrativeStage.CONTEXT)
    
    engine = ConflictEngine()
    conflicts = engine.detect_conflicts([bullish, bearish])
    
    assert len(conflicts) == 1
    assert conflicts[0].concept_name == "Market Context Conflict"
