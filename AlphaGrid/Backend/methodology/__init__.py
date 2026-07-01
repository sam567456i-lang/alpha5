"""Methodology package."""

from .signals import Signal
from .base import AbstractMethodology
from .engine import MethodologyEngine
from .trend_following import TrendFollowingMethodology
from .mean_reversion import MeanReversionMethodology

__all__ = [
    'Signal', 
    'AbstractMethodology', 
    'MethodologyEngine', 
    'TrendFollowingMethodology', 
    'MeanReversionMethodology'
]
