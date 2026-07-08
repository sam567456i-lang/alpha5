from abc import abstractmethod
from typing import Any, Dict, List, Optional
from Backend.platforms.platform8_analysis.frameworks.concept_detector_base import ConceptDetectorBase
from Backend.platforms.platform8_analysis.frameworks.zone_index import ListZoneIndex
from Backend.platforms.platform8_analysis.frameworks.zone_engines import (
    RegistryResolver, OverlapEngine, MergeEngine, SplitEngine, 
    LifecycleEngine, FreshnessEngine, ConfidenceEngine
)
from Backend.shared_domain.contracts.zones.zone_dtos import ZoneDTO

class InvalidZoneInputError(Exception):
    pass

class ZoneDetectorBase(ConceptDetectorBase):
    """
    Universal Spatial Zone Framework Base Class.
    Uses composition (engines) for spatial reasoning instead of inheritance.
    Prohibits raw price candle ingestion—must consume Geometry, Structure, or Liquidity DTOs.
    """
    def __init__(self, registry_data: Dict[str, Any]):
        super().__init__()
        self.resolver = RegistryResolver(registry_data)
        self.overlap_engine = OverlapEngine()
        self.merge_engine = MergeEngine(self.resolver)
        self.split_engine = SplitEngine(self.resolver)
        self.lifecycle_engine = LifecycleEngine(self.resolver)
        self.freshness_engine = FreshnessEngine(self.resolver)
        self.confidence_engine = ConfidenceEngine(self.resolver)
        
        # Spatial Index
        self.index = ListZoneIndex()

    def process_inputs(self, inputs: List[Any]) -> List[ZoneDTO]:
        """
        Main entry point for evaluating zone creation or lifecycle updates.
        Strictly rejects raw price candles.
        """
        for inp in inputs:
            # We enforce that inputs are DTOs from other frameworks, not raw dicts or PriceDTOs.
            if hasattr(inp, 'open') and hasattr(inp, 'close') and not hasattr(inp, 'identity'):
                raise InvalidZoneInputError(f"{self.__class__.__name__} received raw price data. Must consume GeometryDTO, StructureDTO, or LiquidityDTO.")
                
        return self._evaluate_zones(inputs)

    @abstractmethod
    def _evaluate_zones(self, inputs: List[Any]) -> List[ZoneDTO]:
        """
        Detector-specific logic to extract semantic geometry into Zones.
        To be implemented by GapZoneDetector, BlockZoneDetector, etc.
        """
        pass
