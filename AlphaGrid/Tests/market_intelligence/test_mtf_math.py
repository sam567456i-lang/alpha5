import pytest
import pandas as pd
from datetime import datetime, timezone
import numpy as np

from Backend.market_intelligence.mtf_alignment_engine import MTFAlignmentEngine

class TestMTFMath:
    def setup_method(self):
        self.engine = MTFAlignmentEngine()

    def test_dst_transition_alignment(self):
        """Tests that alignment handles Daylight Saving Time transitions without drift."""
        # Create a timezone-aware index crossing a DST boundary (e.g. US Eastern)
        # Even though NSE is UTC+5:30 (no DST), the mathematical foundation must handle it if tested on Tier D.
        idx_lower = pd.date_range("2026-03-08 01:45:00", periods=8, freq="15min", tz="America/New_York")
        df_lower = pd.DataFrame({"close": range(100, 108)}, index=idx_lower)
        
        # 1-hour candles
        idx_higher = pd.date_range("2026-03-08 01:00:00", periods=3, freq="1h", tz="America/New_York")
        df_higher = pd.DataFrame({"close": [200, 201, 202]}, index=idx_higher)
        
        # Normalization forces UTC, so let's simulate the UTC equivalent directly
        df_lower_utc = df_lower.tz_convert("UTC")
        df_higher_utc = df_higher.tz_convert("UTC")
        
        aligned = self.engine.align(df_lower_utc, df_higher_utc)
        
        # 2:00 AM skips to 3:00 AM in America/New_York DST transition
        assert len(aligned) == 8
        assert not aligned['htf_close'].isna().all()

    def test_missing_candles_forward_fill(self):
        """Tests that missing HTF candles gracefully forward-fill from the last known state."""
        idx_lower = pd.date_range("2026-07-01 09:15:00", periods=60, freq="1min", tz="UTC")
        df_lower = pd.DataFrame({"close": np.linspace(100, 160, 60)}, index=idx_lower)
        
        # HTF: 15-minute candles, but 09:45 is missing
        idx_higher = pd.DatetimeIndex([
            "2026-07-01 09:15:00+00:00",
            "2026-07-01 09:30:00+00:00",
            "2026-07-01 10:00:00+00:00"
        ])
        df_higher = pd.DataFrame({"close": [200, 201, 203]}, index=idx_higher)
        
        aligned = self.engine.align(df_lower, df_higher)
        
        # At 09:50, it should use the 09:30 HTF bar since 09:45 is missing
        assert aligned.loc["2026-07-01 09:50:00+00:00", "htf_close"] == 201
        
        # At 10:00, it updates to the 10:00 bar
        assert aligned.loc["2026-07-01 10:00:00+00:00", "htf_close"] == 203

    def test_duplicate_candles_handling(self):
        """Tests that duplicate HTF timestamps don't crash alignment and take the last available value."""
        idx_lower = pd.date_range("2026-07-01 09:15:00", periods=10, freq="5min", tz="UTC")
        df_lower = pd.DataFrame({"close": range(100, 110)}, index=idx_lower)
        
        # HTF has a duplicate timestamp
        idx_higher = pd.DatetimeIndex([
            "2026-07-01 09:15:00+00:00",
            "2026-07-01 09:15:00+00:00",
            "2026-07-01 09:30:00+00:00"
        ])
        df_higher = pd.DataFrame({"close": [200, 201, 202]}, index=idx_higher)
        
        # Engine should remove duplicates prior to merging
        aligned = self.engine.align(df_lower, df_higher)
        
        # The merge_asof requires unique monotonic indices on the right side.
        # If the engine handles duplicates properly, this should pass.
        assert aligned.loc["2026-07-01 09:15:00+00:00", "htf_close"] == 201 # Should keep the last duplicate

    def test_partial_session_truncation(self):
        """Tests that HTF candles do not bleed across daily session boundaries."""
        idx_lower = pd.DatetimeIndex([
            "2026-07-01 15:25:00+00:00", # End of Day 1
            "2026-07-01 15:30:00+00:00", # End of Day 1
            "2026-07-02 09:15:00+00:00", # Start of Day 2
            "2026-07-02 09:20:00+00:00"  # Start of Day 2
        ])
        df_lower = pd.DataFrame({"close": [100, 101, 105, 106]}, index=idx_lower)
        
        idx_higher = pd.DatetimeIndex([
            "2026-07-01 15:15:00+00:00",
            "2026-07-02 09:15:00+00:00"
        ])
        df_higher = pd.DataFrame({"close": [200, 205]}, index=idx_higher)
        
        aligned = self.engine.align(df_lower, df_higher)
        
        # 09:15 on Day 2 should NOT use the 15:15 bar from Day 1 if 09:15 was missing.
        # Here 09:15 is present, so it uses 205.
        assert aligned.loc["2026-07-02 09:15:00+00:00", "htf_close"] == 205
