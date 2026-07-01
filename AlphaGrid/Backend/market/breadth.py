"""Market Breadth Calculator — computes breadth metrics from live quotes."""

from __future__ import annotations

from typing import TYPE_CHECKING
from decimal import Decimal, ROUND_HALF_UP

if TYPE_CHECKING:
    from Shared.models.market import MarketSnapshot


class MarketBreadthCalculator:
    """Calculates market breadth metrics (Advances, Declines, AD Ratio, Score)."""

    @staticmethod
    def calculate_breadth(quotes: list[MarketSnapshot]) -> dict[str, float]:
        """Calculate breadth metrics from a list of live quotes.
        
        A stock is an "advance" if its close (last) price > open price.
        A stock is a "decline" if close < open.
        """
        if not quotes:
            return {
                "advances": 0,
                "declines": 0,
                "unchanged": 0,
                "ad_ratio": 1.0,
                "breadth_score": 0.5,
            }

        advances = 0
        declines = 0
        unchanged = 0

        for quote in quotes:
            if quote.close > quote.open:
                advances += 1
            elif quote.close < quote.open:
                declines += 1
            else:
                unchanged += 1

        total_moved = advances + declines
        ad_ratio = (advances / declines) if declines > 0 else float(advances)
        
        if total_moved > 0:
            breadth_score = advances / total_moved
        else:
            breadth_score = 0.5

        return {
            "advances": advances,
            "declines": declines,
            "unchanged": unchanged,
            "ad_ratio": round(ad_ratio, 2),
            "breadth_score": round(breadth_score, 4),
        }
