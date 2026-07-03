from abc import ABC, abstractmethod
from typing import List, Optional, Any
import pandas as pd

class AbstractGeometryEngine(ABC):
    """Base contract for all Geometry Engines."""
    
    @property
    @abstractmethod
    def engine_name(self) -> str:
        pass
        
    @property
    @abstractmethod
    def version(self) -> str:
        pass

    @abstractmethod
    def process(self, data: pd.DataFrame, context: Any) -> List[Any]:
        """
        Process the dataset and return a list of immutable geometry objects.
        """
        pass

class AbstractSwing(ABC):
    """Contract for a Swing point."""
    @property
    @abstractmethod
    def is_high(self) -> bool: pass

class AbstractStructure(ABC):
    """Contract for Market Structure (BOS/CHOCH/MSS)."""
    pass

class AbstractLiquidity(ABC):
    """Contract for Liquidity Pools (EQH/EQL)."""
    pass

class AbstractImbalance(ABC):
    """Contract for Imbalances (FVG/Volume)."""
    pass

class AbstractZone(ABC):
    """Contract for Zones (Supply/Demand/Premium/Discount)."""
    pass
