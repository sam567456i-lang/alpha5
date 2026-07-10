from typing import List, Any
import math

class SyntheticDatasetGenerator:
    """Generates mathematically perfect data structures for unit testing logic."""
    
    @staticmethod
    def generate_perfect_trend(bars: int, slope: float, noise_variance: float = 0.0) -> List[Any]:
        """Creates a flawless trend without retracements."""
        dataset = []
        for i in range(bars):
            price = 100.0 + (i * slope)
            # Stub mapping to OHLC Schema
            dataset.append({"timestamp": None, "open": price, "high": price + 1, "low": price - 1, "close": price, "volume": 100})
        return dataset
        
    @staticmethod
    def generate_perfect_range(bars: int, center: float, amplitude: float) -> List[Any]:
        """Creates a sine-wave oscillation representing a perfect sideways market."""
        dataset = []
        for i in range(bars):
            price = center + (math.sin(i) * amplitude)
            dataset.append({"timestamp": None, "open": price, "high": price + 1, "low": price - 1, "close": price, "volume": 100})
        return dataset
