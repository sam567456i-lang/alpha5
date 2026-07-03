import pytest
import pandas as pd
from datetime import datetime, timezone
from Backend.market_intelligence.data_quality_gate import DataQualityGate
from Backend.foundation.exceptions import DataError

def test_data_quality_gate():
    gate = DataQualityGate(acceptance_threshold=90.0)
    
    idx = pd.date_range("2026-07-01 09:15:00", periods=5, freq="5min", tz="UTC")
    perfect_df = pd.DataFrame({
        "open": [100]*5,
        "high": [101]*5,
        "low": [99]*5,
        "close": [100]*5,
        "volume": [1000]*5
    }, index=idx)
    
    # Perfect score
    score = gate.calculate_score(perfect_df, expected_bars=5)
    assert score == 100.0
    
    assert gate.evaluate_and_enforce(perfect_df, expected_bars=5, symbol="NIFTY") == True
    
    # Missing bars
    score_missing = gate.calculate_score(perfect_df, expected_bars=10) # 5 missing
    assert score_missing < 100.0
    
    # Bad dataset (below 90)
    bad_df = pd.DataFrame({
        "open": [100]*5,
        "high": [100]*5, # 0 spread
        "low": [100]*5,
        "close": [100]*5,
        "volume": [0]*5 # 0 volume
    }, index=idx)
    
    with pytest.raises(DataError):
        gate.evaluate_and_enforce(bad_df, expected_bars=10, symbol="NIFTY")
