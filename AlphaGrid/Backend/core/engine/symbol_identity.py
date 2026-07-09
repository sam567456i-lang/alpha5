from dataclasses import dataclass

@dataclass(frozen=True)
class SymbolIdentity:
    """
    Objective metadata defining a tradable instrument.
    """
    id: str
    exchange: str
    venue: str
    currency: str
    contract: str
    tick_size: float
    point_value: float
    asset_class: str
    timezone: str
    trading_calendar: str
    session_template: str
    roll_schedule: str
    precision: int
