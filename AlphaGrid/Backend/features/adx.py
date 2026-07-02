"""Average Directional Index (ADX) Feature."""

from collections import deque
from typing import Any, Dict, List
from Shared.models.market import MarketSnapshot
from .base import AbstractFeature

class ADXFeature(AbstractFeature):
    """
    Computes ADX, +DI, and -DI using Wilder's Smoothing.
    O(n) streaming calculation.
    """

    def __init__(self, period: int = 14) -> None:
        self.period = period
        self._prev_high = None
        self._prev_low = None
        self._prev_close = None
        
        self._tr_smooth = 0.0
        self._pdm_smooth = 0.0
        self._ndm_smooth = 0.0
        
        self._dx_values = deque()  # type: ignore
        self._adx = None
        self._bar_count = 0

        # Used for initial simple sum (Wilder's initial smoothing step)
        self._initial_tr = deque()  # type: ignore
        self._initial_pdm = deque()  # type: ignore
        self._initial_ndm = deque()  # type: ignore

    @classmethod
    def get_name(cls) -> str:
        return "ADX_14"

    @classmethod
    def get_version(cls) -> str:
        return "v1"

    @classmethod
    def get_dependencies(cls) -> List[str]:
        return []

    @classmethod
    def warmup_period(cls) -> int:
        return 28  # 14 for +DI/-DI, plus 14 for ADX

    def compute(self, snapshot: MarketSnapshot, dependency_values: Dict[str, Any]) -> Any:
        high = float(snapshot.high)
        low = float(snapshot.low)
        close = float(snapshot.close)
        
        self._bar_count += 1

        if self._prev_close is None:
            self._prev_high = high  # type: ignore
            self._prev_low = low  # type: ignore
            self._prev_close = close  # type: ignore
            return None

        tr = max(high - low, abs(high - self._prev_close), abs(low - self._prev_close))
        
        up_move = high - self._prev_high
        down_move = self._prev_low - low
        
        pdm = up_move if up_move > down_move and up_move > 0 else 0.0
        ndm = down_move if down_move > up_move and down_move > 0 else 0.0

        self._prev_high = high
        self._prev_low = low
        self._prev_close = close

        # Initial accumulation phase for +DI / -DI
        if self._bar_count <= self.period + 1:
            self._initial_tr.append(tr)
            self._initial_pdm.append(pdm)
            self._initial_ndm.append(ndm)
            
            if self._bar_count == self.period + 1:
                self._tr_smooth = sum(self._initial_tr)
                self._pdm_smooth = sum(self._initial_pdm)
                self._ndm_smooth = sum(self._initial_ndm)
                
                self._initial_tr.clear()
                self._initial_pdm.clear()
                self._initial_ndm.clear()
            else:
                return None
        else:
            # Wilder's Smoothing
            self._tr_smooth = self._tr_smooth - (self._tr_smooth / self.period) + tr
            self._pdm_smooth = self._pdm_smooth - (self._pdm_smooth / self.period) + pdm
            self._ndm_smooth = self._ndm_smooth - (self._ndm_smooth / self.period) + ndm

        # Compute +DI and -DI
        pdi = (self._pdm_smooth / self._tr_smooth) * 100 if self._tr_smooth > 0 else 0.0
        ndi = (self._ndm_smooth / self._tr_smooth) * 100 if self._tr_smooth > 0 else 0.0
        
        dx = abs(pdi - ndi) / (pdi + ndi) * 100 if (pdi + ndi) > 0 else 0.0

        # Initial accumulation phase for ADX
        if self._bar_count <= (2 * self.period):
            self._dx_values.append(dx)
            if self._bar_count == (2 * self.period):
                self._adx = sum(self._dx_values) / self.period
                self._dx_values.clear()
                return {"adx": self._adx, "pdi": pdi, "ndi": ndi}
            return None

        # Smoothed ADX
        self._adx = ((self._adx * (self.period - 1)) + dx) / self.period
        return {"adx": self._adx, "pdi": pdi, "ndi": ndi}
