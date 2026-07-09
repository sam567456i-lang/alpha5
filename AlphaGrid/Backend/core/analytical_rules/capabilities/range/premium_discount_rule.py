from enum import Enum
from typing import Optional

from Backend.core.analytical_rules.dto.liquidity.price_observation import PriceObservationDTO
from Backend.core.analytical_rules.dto.range.range_state import RangeState

class RangeZone(Enum):
    PREMIUM = "PREMIUM"
    DISCOUNT = "DISCOUNT"
    EQUILIBRIUM = "EQUILIBRIUM"

class PremiumDiscountRule:
    """
    Objectively determines which RangeZone a given price falls into.
    """
    
    def evaluate(self, range_state: RangeState, observation: PriceObservationDTO) -> RangeZone:
        # We can use the 'close' or 'midpoint' of the candle.
        # Let's use the typical price or close price. For now, typical price:
        typical_price = (observation.high + observation.low + observation.close) / 3.0
        
        if typical_price > range_state.premium_threshold:
            return RangeZone.PREMIUM
        elif typical_price < range_state.discount_threshold:
            return RangeZone.DISCOUNT
        else:
            return RangeZone.EQUILIBRIUM
