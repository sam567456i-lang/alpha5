from dataclasses import dataclass

@dataclass
class SwingValidationPolicy:
    """Configurable policy dictating what makes a raw swing statistically significant."""
    min_amplitude_atr: float = 1.5
    min_duration_bars: int = 3
    require_close_confirmation: bool = True
