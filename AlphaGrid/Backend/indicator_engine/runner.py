from typing import Dict, Any, Optional
from Backend.indicator_engine.factory import IndicatorFactory
from Backend.indicator_engine.results import FinancialIndicatorResult
from Backend.market_data.market_series import MarketSeries
from Backend.market_data.market_dataset import MarketDataset

class IndicatorRunner:
    """Orchestrates execution of Indicator Engines."""
    
    @classmethod
    def execute(
        cls, 
        indicator_id: str, 
        series: MarketSeries, 
        context: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> FinancialIndicatorResult:
        """
        Executes a registered indicator engine.
        
        Args:
            indicator_id: The registered ID of the indicator (e.g., 'macd', 'roc').
            series: The immutable MarketSeries contract.
            context: Optional execution context (e.g., trace IDs, etc.).
            kwargs: Parameters for the indicator engine constructor.
            
        Returns:
            A subclass of FinancialIndicatorResult containing the numerical arrays.
        """
        engine = IndicatorFactory.get_instance(indicator_id, **kwargs)
        # All engines must expose a generate() method taking a MarketSeries
        return engine.generate(series)
