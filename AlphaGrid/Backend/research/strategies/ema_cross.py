"""Golden Strategy: Dual EMA Crossover for E2E verification."""

from datetime import timedelta
from typing import Dict, Any, List
import numpy as np

from Backend.research.engine.strategy_interface import AbstractStrategy, STRATEGY_REGISTRY


class EMACrossStrategy(AbstractStrategy):
    """
    A canonical Golden Strategy for E2E testing.
    Purely reactive: computes short/long moving averages and generates
    crossover signals. No forward-looking labels.
    """

    @classmethod
    def get_parameter_schema(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "short_window": {"type": int, "required": True, "min": 1, "max": 50},
            "long_window": {"type": int, "required": True, "min": 10, "max": 200}
        }

    @classmethod
    def max_label_horizon(cls) -> timedelta:
        """Purely reactive — no forward-looking labels."""
        return timedelta(0)

    def __init__(self, parameters: Dict[str, Any], random_generator: np.random.Generator | None = None) -> None:

        super().__init__(parameters, random_generator)
        self.short_window = parameters.get("short_window", 10)
        self.long_window = parameters.get("long_window", 50)

        self.prices: List[float] = []
        self.signals: List[Dict[str, Any]] = []
        self.trades: List[Dict[str, Any]] = []
        self.position = 0  # 1 = long, 0 = flat
        self._entry_price = 0.0
        self._entry_ts = None

    def _sma(self, window: int) -> float:
        """Simple moving average over the trailing window."""
        if len(self.prices) < window:
            return 0.0
        return sum(self.prices[-window:]) / window

    def on_market_event(self, event: Dict[str, Any]) -> None:
        price = event.get("close", 0.0)
        ts = event.get("timestamp")
        if price <= 0:
            return

        self.prices.append(price)

        if len(self.prices) < self.long_window:
            return

        short_ma = self._sma(self.short_window)
        long_ma = self._sma(self.long_window)

        # Golden Cross -> Buy
        if short_ma > long_ma and self.position == 0:
            self.position = 1
            self._entry_price = price
            self._entry_ts = ts
            self.signals.append({"timestamp": ts, "direction": "BUY", "price": price})

        # Death Cross -> Sell
        elif short_ma < long_ma and self.position == 1:
            pnl = price - self._entry_price
            self.trades.append({
                "instrument": event.get("symbol", "BTCUSDT"),
                "direction": "LONG",
                "entry_timestamp": self._entry_ts,
                "exit_timestamp": ts,
                "entry_price": self._entry_price,
                "exit_price": price,
                "quantity": 1.0,
                "pnl": pnl,
                "exit_reason": "SIGNAL"
            })
            self.signals.append({"timestamp": ts, "direction": "SELL", "price": price})
            self.position = 0
            self._entry_price = 0.0
            self._entry_ts = None


STRATEGY_REGISTRY.register("EMA_CROSS", EMACrossStrategy)
