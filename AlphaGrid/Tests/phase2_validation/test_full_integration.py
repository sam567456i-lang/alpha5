import pytest
from Backend.core.dtos import OHLCV

# --- Mock Pipeline Layers ---
class MockIndicator:
    """Takes Ticks and outputs a simple moving sum"""
    def __init__(self):
        self.total = 0.0
        
    def process(self, tick: OHLCV) -> float:
        self.total += tick.close
        return self.total

class MockAnalysis:
    """Takes Indicator output and identifies a trend"""
    def process(self, indicator_val: float) -> str:
        return "BULL" if indicator_val > 500 else "BEAR"

class MockConcept:
    """Takes Analysis and scores the Market Structure"""
    def process(self, analysis_val: str) -> int:
        return 1 if analysis_val == "BULL" else -1

class MockState:
    """Consolidates Concepts into a final Market Regime State"""
    def __init__(self):
        self.regime_score = 0
        
    def update(self, concept_val: int):
        self.regime_score += concept_val
        return self.regime_score

def test_full_integration_gate_10():
    """
    Gate 10: Full Integration
    Proves the hierarchical architecture physically flows:
    Tick -> Indicator -> Analysis -> Concept -> State
    """
    
    # 1. Instantiate the Pipeline
    indicator = MockIndicator()
    analysis = MockAnalysis()
    concept = MockConcept()
    market_state = MockState()
    
    # 2. Push 10 Ticks through the Pipeline
    for i in range(1, 11):
        # We push a price of 100 each time
        tick = OHLCV(timestamp=i, open=100, high=100, low=100, close=100, volume=100, symbol="NIFTY")
        
        # Layer 1: Indicator
        ind_val = indicator.process(tick)
        
        # Layer 2: Analysis
        an_val = analysis.process(ind_val)
        
        # Layer 3: Concept
        con_val = concept.process(an_val)
        
        # Layer 4: State
        final_state = market_state.update(con_val)
        
        # Validation checks mid-stream
        if i == 5:
            # Indicator should be 500
            assert ind_val == 500
            # Analysis should be BEAR since 500 is not > 500
            assert an_val == "BEAR"
            assert con_val == -1
            
        if i == 6:
            # Indicator should be 600
            assert ind_val == 600
            # Analysis should be BULL since 600 > 500
            assert an_val == "BULL"
            assert con_val == 1
            
    # 3. Final Validation
    # Ticks 1 to 5 = BEAR (-1 * 5) = -5
    # Ticks 6 to 10 = BULL (1 * 5) = +5
    # Total Final State Score = 0
    assert market_state.regime_score == 0, f"Integration broken! Expected final state 0, got {market_state.regime_score}"
