"""
Data Quality Gate.

Purpose
-------
Implements the standardized Data Quality Score formula:
(Missing Bars 20%) + (Duplicates 15%) + (Latency 15%) + (Spread 20%) + (Volume 15%) + (Corporate Actions 15%)
Enforces a strict Accept/Reject threshold before data is consumed downstream.

Consumes
--------
Canonical OHLCV DataFrame
DataProvenanceTracker

Produces
--------
Data Quality Score, Acceptance Boolean

Registry
--------
MarketIntelligenceRegistry

Downstream
----------
FeatureEngine

Inputs
------
df (pd.DataFrame), expected_bars (int), symbol (str)

Outputs
-------
bool

Failure Modes
-------------
Score < Threshold -> DataError

Complexity
----------
Time: O(N)
Space: O(1)

Thread Safety
-------------
Yes - Stateless evaluation.

Determinism
-----------
Deterministic based on score formula.

Version
-------
1.0.0

Tests
-----
tests/market_intelligence/test_data_quality_gate.py
"""

import pandas as pd
from typing import Dict, Any

from Backend.foundation.exceptions import DataError

class DataQualityGate:
    """Enforces data quality thresholds based on the canonical scoring formula."""

    def __init__(self, acceptance_threshold: float = 90.0):
        """
        Initializes the Data Quality Gate.
        
        Args:
            acceptance_threshold (float): Minimum score (out of 100) to accept a dataset.
        """
        self._threshold = acceptance_threshold

    def calculate_score(self, df: pd.DataFrame, expected_bars: int) -> float:
        """
        Calculates the Data Quality Score for a given dataset.
        
        Args:
            df (pd.DataFrame): The dataset to evaluate.
            expected_bars (int): The number of bars expected in this time window.
            
        Returns:
            float: The score out of 100.
        """
        if df.empty or expected_bars <= 0:
            return 0.0

        actual_bars = len(df)
        
        # 1. Missing Bars (Weight: 20%)
        # Score is 20 if all bars present, drops linearly
        missing_ratio = max(0.0, (expected_bars - actual_bars) / expected_bars)
        missing_score = 20.0 * (1.0 - missing_ratio)

        # 2. Duplicates (Weight: 15%)
        # Assumes normalization engine already removed duplicates, but we check if they *were* present
        # If index has duplicates, score drops. 
        duplicate_ratio = df.index.duplicated().sum() / actual_bars
        duplicate_score = 15.0 * (1.0 - min(1.0, duplicate_ratio * 5)) # Heavily penalize duplicates

        # 3. Latency (Weight: 15%)
        # Placeholder: Assume 15/15 for historical data. Live data would check arrival time vs timestamp.
        latency_score = 15.0

        # 4. Spread (Weight: 20%)
        # Placeholder: Check if High/Low spread is realistic (e.g., no 0 spread bars unless illiquid)
        zero_spread_ratio = (df['high'] == df['low']).sum() / actual_bars
        spread_score = 20.0 * (1.0 - min(1.0, zero_spread_ratio * 2))

        # 5. Volume (Weight: 15%)
        # Penalize zero volume bars
        zero_volume_ratio = (df['volume'] == 0).sum() / actual_bars
        volume_score = 15.0 * (1.0 - zero_volume_ratio)

        # 6. Corporate Actions (Weight: 15%)
        # Placeholder: Assume corporate actions correctly applied for now.
        corp_action_score = 15.0
        
        total_score = missing_score + duplicate_score + latency_score + spread_score + volume_score + corp_action_score
        return max(0.0, min(100.0, total_score))

    def evaluate_and_enforce(self, df: pd.DataFrame, expected_bars: int, symbol: str) -> bool:
        """
        Evaluates the dataset and raises an error if it falls below the threshold.
        
        Args:
            df (pd.DataFrame): The dataset to evaluate.
            expected_bars (int): The expected number of bars.
            symbol (str): The symbol being evaluated.
            
        Returns:
            bool: True if accepted.
            
        Raises:
            DataError: If the score is strictly below the acceptance threshold.
        """
        score = self.calculate_score(df, expected_bars)
        
        if score < self._threshold:
            raise DataError(
                f"Data Quality Gate Failed for {symbol}. "
                f"Score {score:.2f} < Threshold {self._threshold:.2f}."
            )
            
        return True
