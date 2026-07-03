"""Price Action Concept Generator."""

from typing import Any, Dict, List, Deque
from collections import deque
from datetime import datetime
import uuid
import numpy as np

from Backend.concepts.base import Concept
from Backend.concepts.generator import AbstractConceptGenerator
from Shared.enums.concept_type import ConceptType


class PriceActionConceptGenerator(AbstractConceptGenerator):
    """
    Generates Candlestick Pattern Concepts.
    Consumes raw OHLC feature outputs (e.g., from a Passthrough feature).
    """

    def __init__(self, open_source: str = "open", high_source: str = "high", 
                 low_source: str = "low", close_source: str = "close") -> None:
        self.open_src = open_source
        self.high_src = high_source
        self.low_src = low_source
        self.close_src = close_source
        
        # Keep last 3 bars for patterns like Engulfing, Morning Star, etc.
        self._history: Deque[Dict[str, float]] = deque(maxlen=3)

    def get_id(self) -> str:
        return "PriceActionPatterns"

    def get_version(self) -> str:
        return "v2"

    def get_required_features(self) -> List[str]:
        return [self.open_src, self.high_src, self.low_src, self.close_src]

    def evaluate(self, timestamp: datetime, feature_values: Dict[str, Any], geometry_cache: Any = None) -> Concept:
        o = float(feature_values[self.open_src])
        h = float(feature_values[self.high_src])
        l = float(feature_values[self.low_src])
        c = float(feature_values[self.close_src])
        
        current_bar = {"open": o, "high": h, "low": l, "close": c}
        self._history.append(current_bar)
        
        state = "NEUTRAL"
        confidence = 0.5
        pattern_name = "NONE"
        is_bullish = False
        
        t_size = h - l
        b_size = abs(c - o)
        
        # Avoid division by zero
        t_size_safe = t_size if t_size > 0 else 0.0001
        
        u_shadow = h - c if c >= o else h - o
        l_shadow = o - l if c >= o else c - l
        
        # Single bar patterns
        if l_shadow / t_size_safe > 0.6 and u_shadow / t_size_safe < 0.2:
            state = "HAMMER"
            pattern_name = "HAMMER"
            is_bullish = True
            confidence = 0.8
        elif u_shadow / t_size_safe > 0.6 and l_shadow / t_size_safe < 0.2:
            state = "SHOOTING_STAR"
            pattern_name = "SHOOTING_STAR"
            is_bullish = False
            confidence = 0.8
        elif b_size / t_size_safe < 0.1 and t_size > 0:
            state = "DOJI"
            pattern_name = "DOJI"
            confidence = 0.6
            
        # Two bar patterns
        if len(self._history) >= 2 and state == "NEUTRAL":
            prev = self._history[-2]
            prev_b_size = abs(prev["close"] - prev["open"])
            
            # Engulfing
            if b_size > prev_b_size:
                if c > o and prev["close"] < prev["open"]:
                    if c > prev["open"] and o < prev["close"]:
                        state = "BULLISH_ENGULFING"
                        pattern_name = "BULLISH_ENGULFING"
                        is_bullish = True
                        confidence = 0.85
                elif c < o and prev["close"] > prev["open"]:
                    if c < prev["open"] and o > prev["close"]:
                        state = "BEARISH_ENGULFING"
                        pattern_name = "BEARISH_ENGULFING"
                        is_bullish = False
                        confidence = 0.85

        concept_type = getattr(ConceptType, 'PRICE_ACTION', ConceptType.UNKNOWN)
        
        return Concept(
            id=f"{self.get_id()}_{state}",
            type=concept_type,
            version=self.get_version(),
            timestamp=timestamp,
            confidence=confidence,
            inputs={"pattern": pattern_name, "is_bullish": is_bullish, "size": t_size},
            generator=self.__class__.__name__,
            geometry_dependencies=[]
        )
