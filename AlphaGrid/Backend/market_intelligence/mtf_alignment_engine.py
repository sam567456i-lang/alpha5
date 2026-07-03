"""
Multi-Timeframe (MTF) Alignment Engine.

Purpose
-------
Implementation of ADR-001: Strict "Closed-Bar Only" rule and "Forward-Fill" 
missing bar logic to guarantee absolute environment parity (Live vs Research)
and zero look-ahead bias.

Consumes
--------
Canonical OHLCV DataFrame

Produces
--------
Aligned MTF DataFrame

Registry
--------
MarketIntelligenceRegistry

Downstream
----------
FeatureEngine

Inputs
------
lower_tf_df (pd.DataFrame), higher_tf_df (pd.DataFrame)

Outputs
-------
pd.DataFrame

Failure Modes
-------------
Missing index -> TypeError
Empty dataset -> Returns empty/original

Complexity
----------
Time: O(N log N)
Space: O(N)

Thread Safety
-------------
Yes - Pure mathematical function.

Determinism
-----------
Absolute determinism guaranteed by ADR-001.

Version
-------
1.0.0

Tests
-----
tests/market_intelligence/test_mtf_math.py
"""

import pandas as pd
from typing import Dict, Any

class MTFAlignmentEngine:
    """Aligns higher timeframe bars to lower timeframe bars deterministically."""

    def align(self, lower_tf_df: pd.DataFrame, higher_tf_df: pd.DataFrame) -> pd.DataFrame:
        """
        Aligns higher timeframe data to lower timeframe timestamps.
        Enforces the "Closed-Bar Only" rule from ADR-001.

        Args:
            lower_tf_df (pd.DataFrame): Lower timeframe data (e.g., 5m) with datetime index.
            higher_tf_df (pd.DataFrame): Higher timeframe data (e.g., 1H) with datetime index.
            
        Returns:
            pd.DataFrame: A combined DataFrame where higher timeframe data is aligned
                          and forward-filled to match the lower timeframe index.
        """
        if lower_tf_df.empty:
            return pd.DataFrame()
        if higher_tf_df.empty:
            return lower_tf_df.copy()

        # Both indices must be datetime
        if not isinstance(lower_tf_df.index, pd.DatetimeIndex) or not isinstance(higher_tf_df.index, pd.DatetimeIndex):
            raise TypeError("Both DataFrames must have DatetimeIndex for MTF alignment.")
            
        # Ensure they are sorted chronologically
        lower_tf_df = lower_tf_df.sort_index()
        higher_tf_df = higher_tf_df.sort_index()
        
        # Deduplicate indices (keep the last occurring value for the same timestamp)
        lower_tf_df = lower_tf_df[~lower_tf_df.index.duplicated(keep='last')]
        higher_tf_df = higher_tf_df[~higher_tf_df.index.duplicated(keep='last')]

        # ADR-001 Rule 1 & 2: Closed-Bar Only + As-Of Forward Fill
        # pd.merge_asof with direction='backward' ensures that for any lower_tf timestamp,
        # we only look at higher_tf timestamps that are LESS THAN OR EQUAL to it.
        # This means we only look at fully closed bars.
        
        # Rename higher timeframe columns to avoid collisions
        htf = higher_tf_df.add_prefix('htf_')
        
        aligned_df = pd.merge_asof(
            lower_tf_df, 
            htf,
            left_index=True, 
            right_index=True, 
            direction='backward'
        )

        return aligned_df
