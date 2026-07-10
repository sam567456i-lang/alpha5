from typing import List, Any
import random

class DatasetBuilder:
    """Chunks and injects stress onto raw Phase 2A data to produce research assets."""
    
    @staticmethod
    def inject_stress(dataset: List[Any], missing_probability: float = 0.05) -> List[Any]:
        """Simulates feed disconnects by randomly dropping bars."""
        return [bar for bar in dataset if random.random() > missing_probability]
        
    @staticmethod
    def create_walk_forward_splits(dataset: List[Any], train_pct: float = 0.6, val_pct: float = 0.2):
        """Splits data strictly chronologically to prevent data leakage."""
        total = len(dataset)
        train_end = int(total * train_pct)
        val_end = train_end + int(total * val_pct)
        
        return {
            "train": dataset[:train_end],
            "validation": dataset[train_end:val_end],
            "test": dataset[val_end:]
        }
