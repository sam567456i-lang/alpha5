import pytest
import pandas as pd
from datetime import datetime, timezone

from Backend.market_intelligence.normalization_engine import NormalizationEngine
from Backend.foundation.exceptions import DataError

class TestFailureSuite:
    def setup_method(self):
        self.engine = NormalizationEngine()
        self.idx = pd.date_range("2026-07-01 09:15:00", periods=5, freq="5min", tz="UTC")
        self.valid_df = pd.DataFrame({
            "open": [100]*5,
            "high": [101]*5,
            "low": [99]*5,
            "close": [100]*5,
            "volume": [1000]*5
        }, index=self.idx)

    def test_reject_negative_prices(self):
        df = self.valid_df.copy()
        df.iloc[2, df.columns.get_loc('close')] = -5.0 # Negative close
        
        with pytest.raises(DataError, match="Negative prices detected"):
            self.engine.normalize(df, symbol="NIFTY", timeframe="5m")

    def test_reject_naive_timezone(self):
        df = self.valid_df.copy()
        df.index = df.index.tz_localize(None) # Make timezone naive
        
        with pytest.raises(DataError, match="Timezone naive data detected"):
            self.engine.normalize(df, symbol="NIFTY", timeframe="5m")

    def test_reject_duplicate_timestamps(self):
        df = self.valid_df.copy()
        # Create a duplicate index
        duplicate_idx = list(self.idx)
        duplicate_idx[2] = duplicate_idx[1]
        df.index = pd.DatetimeIndex(duplicate_idx)
        
        with pytest.raises(DataError, match="Duplicate timestamps detected"):
            self.engine.normalize(df, symbol="NIFTY", timeframe="5m")

    def test_reject_missing_metadata_columns(self):
        df = self.valid_df.copy()
        df.drop(columns=['volume'], inplace=True)
        
        with pytest.raises(DataError, match="Missing required columns"):
            self.engine.normalize(df, symbol="NIFTY", timeframe="5m")
            
    def test_reject_empty_dataset(self):
        df = pd.DataFrame()
        with pytest.raises(DataError, match="is empty"):
            self.engine.normalize(df, symbol="NIFTY", timeframe="5m")
