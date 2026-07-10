from typing import List, Optional
from abc import ABC, abstractmethod

class LiquiditySDK(ABC):
    """
    The only interface Platform 11 uses to interact with Liquidity Objects.
    Implementation details, caching, and extraction rules remain hidden.
    """
    
    @abstractmethod
    def get_reference_levels(self, start_time, end_time) -> List:
        """Returns ReferenceLevel objects within the time window."""
        pass
        
    @abstractmethod
    def get_swing_liquidity(self, start_time, end_time) -> List:
        """Returns SwingLiquidity objects."""
        pass
        
    @abstractmethod
    def get_session_liquidity(self, session_id: str, start_time, end_time) -> List:
        """Returns SessionLiquidity objects for a specific TradingSession."""
        pass
        
    @abstractmethod
    def get_range_liquidity(self, range_id: str) -> List:
        """Returns RangeLiquidity objects for a specific Range."""
        pass
        
    @abstractmethod
    def get_liquidity_pools(self, start_time, end_time) -> List:
        """Returns Composition-based LiquidityPool objects."""
        pass
