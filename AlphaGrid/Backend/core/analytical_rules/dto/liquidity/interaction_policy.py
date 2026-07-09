from dataclasses import dataclass

@dataclass(frozen=True)
class InteractionPolicy:
    """
    Defines the rigorous boundaries for an interaction rule without hardcoding concepts.
    """
    touch_definition: str = "EXTREMES_ONLY" # e.g. EXTREMES_ONLY (High/Low), BODY_INCLUSIVE (Open/Close)
    penetration_definition: str = "ANY"
    boundary_source: str = "OUTER_BOUND" # e.g. OUTER_BOUND (upper_bound for BuySide, lower_bound for SellSide), CENTER_PRICE
    measurement_source: str = "EXTREME_PRICE" # e.g. EXTREME_PRICE, CLOSE_PRICE
    minimum_penetration: float = 0.0
    minimum_duration: int = 0
    price_reference: str = "ABSOLUTE"
