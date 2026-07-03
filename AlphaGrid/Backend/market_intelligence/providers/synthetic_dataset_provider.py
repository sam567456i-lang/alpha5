"""Deterministic synthetic dataset provider for development and CI."""

import json
import os
import pandas as pd
from datetime import datetime

from Backend.market_intelligence.providers.abstract_market_data_provider import HistoricalDataProvider
from Backend.market_intelligence.providers.provider_factory import ProviderFactory

class SyntheticDatasetProvider(HistoricalDataProvider):
    """
    Deterministic provider serving the golden dataset.
    Purpose: deterministic development, CI, architecture pipeline verification.
    """
    
    @property
    def provider_id(self) -> str:
        return "SYNTHETIC_GOLDEN"
        
    @property
    def dataset_version(self) -> str:
        return "1.0.0"

    def get_historical_bars(self, symbol: str, start_time: datetime, end_time: datetime, timeframe: str) -> pd.DataFrame:
        path = os.path.join(
            os.path.dirname(__file__), "..", "..", "tests", "golden_data", "BTCUSDT_1H_GOLDEN.json"
        )
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        df = pd.DataFrame(data)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df.set_index("timestamp", inplace=True)
        df.sort_index(inplace=True)
        
        # Filter logic to return only rows between start_time and end_time
        mask = (df.index >= start_time) & (df.index <= end_time)
        return df.loc[mask]

# Auto-register this plugin with the factory
ProviderFactory.register("synthetic", SyntheticDatasetProvider)
