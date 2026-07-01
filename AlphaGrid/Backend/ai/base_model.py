"""Base AI Model Interface."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
import numpy as np


class AbstractAIModel(ABC):
    """
    Abstract interface for all ML models.
    Enforces the Progression Rules (Rule -> Linear -> Logic -> Tree -> Forest -> Boosting -> NN).
    """

    @classmethod
    @abstractmethod
    def get_family(cls) -> str:
        """Returns the ML family (e.g., 'LinearRegression', 'RandomForest')."""
        pass

    @abstractmethod
    def train(self, features: np.ndarray, labels: np.ndarray) -> Dict[str, float]:
        """
        Trains the model offline.
        
        Args:
            features: 2D numpy array of normalized features.
            labels: 1D numpy array of target labels.
            
        Returns:
            Dictionary of training metrics (e.g., loss, accuracy).
        """
        pass

    @abstractmethod
    def predict(self, features: np.ndarray) -> Tuple[str, float]:
        """
        Runs inference on new data.
        
        Args:
            features: 2D numpy array of features for a single event.
            
        Returns:
            Tuple of (direction, confidence).
        """
        pass
