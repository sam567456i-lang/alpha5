import pandas as pd
import pytest
from datetime import datetime, timezone
from typing import Dict, Any

from Backend.market_intelligence.mtf_alignment_engine import MTFAlignmentEngine

def test_mtf_alignment_no_lookahead():
    """
    Tests that MTF Alignment strictly follows the 'Closed-Bar Only' rule 
    (ADR-001) and does not leak future information.
    """
    engine = MTFAlignmentEngine()
    
    # 5-minute bars (lower timeframe)
    lower_idx = pd.date_range("2026-07-01 09:15:00", periods=5, freq="5min", tz="UTC")
    lower_df = pd.DataFrame({
        "open": [100, 101, 102, 103, 104],
        "close": [101, 102, 103, 104, 105]
    }, index=lower_idx)
    
    # 15-minute bars (higher timeframe)
    higher_idx = pd.date_range("2026-07-01 09:15:00", periods=2, freq="15min", tz="UTC")
    higher_df = pd.DataFrame({
        "open": [100, 103],
        "close": [103, 106]
    }, index=higher_idx)
    
    aligned = engine.align(lower_df, higher_df)
    
    # Assertions
    # At 09:15, higher timeframe bar for 09:15 is available
    assert aligned.loc["2026-07-01 09:15:00+00:00", "htf_close"] == 103
    
    # At 09:20 and 09:25, we should STILL be using the 09:15 bar (forward fill)
    assert aligned.loc["2026-07-01 09:20:00+00:00", "htf_close"] == 103
    assert aligned.loc["2026-07-01 09:25:00+00:00", "htf_close"] == 103
    
    # At 09:30, the 09:30 htf bar becomes available
    assert aligned.loc["2026-07-01 09:30:00+00:00", "htf_close"] == 106

def test_mtf_alignment_empty_data():
    engine = MTFAlignmentEngine()
    empty = pd.DataFrame()
    
    lower_idx = pd.date_range("2026-07-01 09:15:00", periods=1, freq="5min", tz="UTC")
    lower_df = pd.DataFrame({"close": [100]}, index=lower_idx)
    
    assert engine.align(empty, empty).empty
    assert engine.align(empty, lower_df).empty
    assert len(engine.align(lower_df, empty)) == 1
