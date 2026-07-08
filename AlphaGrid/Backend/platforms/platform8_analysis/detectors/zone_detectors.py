from typing import List, Any
from Backend.platforms.platform8_analysis.frameworks.zone_detector_base import ZoneDetectorBase
from Backend.shared_domain.contracts.zones.zone_dtos import ZoneDTO

class GapZoneDetector(ZoneDetectorBase):
    """
    Detects spatial gaps from structural and liquidity inputs.
    Generic. Methodology mappings occur in Platform 10.
    """
    def _evaluate_zones(self, inputs: List[Any]) -> List[ZoneDTO]:
        results = []
        return results

class BlockZoneDetector(ZoneDetectorBase):
    """
    Detects volumetric and geometric blocks (e.g., accumulation nodes).
    Generic. Methodology mappings occur in Platform 10.
    """
    def _evaluate_zones(self, inputs: List[Any]) -> List[ZoneDTO]:
        results = []
        return results
