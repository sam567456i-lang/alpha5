"""Canonical Historical Market Pipeline."""

from datetime import datetime
from typing import Any, Dict, List

from Backend.market_intelligence.providers.abstract_market_data_provider import HistoricalDataProvider
from Backend.market_intelligence.normalization_engine import NormalizationEngine
from Backend.market_intelligence.session_engine import SessionEngine
from Backend.market_intelligence.data_quality_gate import DataQualityGate
from Backend.foundation.exceptions import DataError

class HistoricalMarketPipeline:
    """
    Encapsulates the canonical sequence of data retrieval, normalization, 
    and quality validation, acting as the domain orchestrator.
    """
    def __init__(
        self,
        provider: HistoricalDataProvider,
        normalization_engine: NormalizationEngine,
        session_engine: SessionEngine,
        data_quality_gate: DataQualityGate
    ):
        self._provider = provider
        self._normalization = normalization_engine
        self._session_engine = session_engine
        self._quality_gate = data_quality_gate

    def execute(
        self, 
        symbol: str, 
        timeframe: str, 
        start_date: str | None = None, 
        end_date: str | None = None
    ) -> List[Dict[str, Any]]:
        """Execute the canonical market data pipeline."""
        
        from datetime import timezone
        
        # 1. Parse dates (fallback to defaults if None)
        if start_date is None or end_date is None:
            # For this verification phase, we require explicit dates to ensure deterministic execution
            raise ValueError("start_date and end_date must be explicitly provided.")
            
        start_time = datetime.fromisoformat(start_date).replace(tzinfo=timezone.utc)
        end_time = datetime.fromisoformat(end_date).replace(tzinfo=timezone.utc)
        
        # 2. Provider Retrieval
        raw_df = self._provider.get_historical_bars(symbol, start_time, end_time, timeframe)
        if raw_df.empty:
            raise DataError(f"No data returned for {symbol} from provider {self._provider.provider_id}")

        # 3. Normalization
        normalized_df = self._normalization.normalize(raw_df, symbol, timeframe)

        # 4. Session Alignment (Calculate expected bars for Data Quality)
        expected_bars = self._session_engine.calculate_expected_bars(start_time, end_time, timeframe)

        # 5. Data Quality
        self._quality_gate.evaluate_and_enforce(normalized_df, expected_bars, symbol)

        # 6. Convert to API Response Format
        # Output consumed by next layer
        df_out = normalized_df.copy()
        df_out.index = df_out.index.map(lambda t: t.isoformat())
        records = df_out.reset_index().to_dict(orient="records")
        return records
