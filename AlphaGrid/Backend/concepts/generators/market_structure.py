"""Market Structure Concept Generator."""

from typing import Any, Dict, List, Optional
from datetime import datetime
import uuid

from Backend.concepts.base import Concept
from Backend.concepts.generator import AbstractConceptGenerator
from Shared.enums.concept_type import ConceptType
from Backend.price_geometry.objects import LifecycleState

class MarketStructureConceptGenerator(AbstractConceptGenerator):
    """
    Consumes the GeometryCache to generate a purely generic, methodology-agnostic
    Market Structure State concept. It exposes atomic states (OBs, FVGs, Liquidity, BOS)
    for downstream Methodologies (SMC, Wyckoff, etc.) to combine into signals.
    """

    def __init__(self, close_source: str = "close") -> None:
        self.close_src = close_source

    def get_id(self) -> str:
        return "MarketStructureState"

    def get_version(self) -> str:
        return "v3.0.0"

    def get_required_features(self) -> List[str]:
        return [self.close_src]

    def evaluate(self, timestamp: datetime, feature_values: Dict[str, Any], geometry_cache: Any = None) -> Concept:
        price = float(feature_values.get(self.close_src, 0.0))
        deps = []
        
        state = {
            "price": price,
            "latest_structure": None,
            "active_order_blocks": [],
            "unmitigated_fvgs": [],
            "active_liquidity_pools": []
        }
        
        if geometry_cache:
            # 1. Latest Structure (BOS / CHOCH)
            structures = geometry_cache.get_by_type("Structure")
            active_structs = [s for s in structures if s.timestamp <= timestamp and s.lifecycle_state == LifecycleState.CONFIRMED]
            if active_structs:
                latest = active_structs[-1]
                state["latest_structure"] = {
                    "type": latest.structure_type,
                    "is_bullish": latest.is_bullish,
                    "price": latest.price,
                    "id": latest.id
                }
                deps.append(latest.id)
                
            # 2. Active Order Blocks
            obs = geometry_cache.get_by_type("OrderBlock")
            active_obs = [ob for ob in obs if ob.timestamp <= timestamp and ob.lifecycle_state in (LifecycleState.CONFIRMED, LifecycleState.MITIGATED)]
            for ob in active_obs:
                state["active_order_blocks"].append({
                    "id": ob.id,
                    "is_bullish": ob.is_bullish,
                    "top": ob.top_price,
                    "bottom": ob.bottom_price,
                    "state": ob.lifecycle_state.value
                })
                deps.append(ob.id)
                
            # 3. Unmitigated FVGs
            fvgs = geometry_cache.get_by_type("Imbalance")
            active_fvgs = [fvg for fvg in fvgs if fvg.timestamp <= timestamp and fvg.lifecycle_state == LifecycleState.CONFIRMED]
            for fvg in active_fvgs:
                state["unmitigated_fvgs"].append({
                    "id": fvg.id,
                    "is_bullish": fvg.is_bullish,
                    "top": fvg.top_price,
                    "bottom": fvg.bottom_price,
                    "filled_pct": getattr(fvg, 'filled_pct', 0.0)
                })
                deps.append(fvg.id)
                
            # 4. Active Liquidity Pools
            pools = geometry_cache.get_by_type("Liquidity")
            active_pools = [p for p in pools if p.timestamp <= timestamp and p.lifecycle_state == LifecycleState.CONFIRMED]
            for p in active_pools:
                state["active_liquidity_pools"].append({
                    "id": p.id,
                    "type": getattr(p, 'pool_type', "UNKNOWN"),
                    "price": p.price
                })
                deps.append(p.id)

        # Deduplicate dependencies
        deps = list(set(deps))

        return Concept(
            id=f"{self.get_id()}_{timestamp.isoformat()}",
            type=getattr(ConceptType, 'MARKET_STRUCTURE', ConceptType.UNKNOWN),
            version=self.get_version(),
            timestamp=timestamp,
            confidence=1.0, # Atomic state is purely factual geometry
            inputs=state,
            generator=self.__class__.__name__,
            geometry_dependencies=deps
        )
