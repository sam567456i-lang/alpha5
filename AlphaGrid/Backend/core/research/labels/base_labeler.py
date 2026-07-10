from abc import ABC, abstractmethod
from typing import List, Any
from Backend.core.research.labels.label import Label

class BaseLabeler(ABC):
    """
    Abstract contract for generating ground truth labels. 
    Labelers are permitted to use future lookahead data, as they 
    exist exclusively in the research validation phase, not detection.
    """
    
    def __init__(self, generator_version: str, policy_version: str):
        self.generator_version = generator_version
        self.policy_version = policy_version
        
    @abstractmethod
    def generate_labels(self, target_objects: List[Any], dataset: Any) -> List[Label]:
        """
        Parses the dataset (with lookahead) to return immutable Label objects
        for the given target objects (e.g., LiquidityLevels).
        """
        pass
