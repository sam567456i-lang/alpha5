from typing import List, Any
from Backend.core.research.labels.base_labeler import BaseLabeler
from Backend.core.research.labels.label import Label
import time

class LiquidityReactionLabeler(BaseLabeler):
    """
    Specifically tests the reaction to LiquidityLevels for EXP-000002.
    """
    
    def __init__(self, reaction_ticks: int = 8, reaction_window_bars: int = 20):
        super().__init__(generator_version="1.0.0", policy_version="LP-0004")
        self.reaction_ticks = reaction_ticks
        self.reaction_window_bars = reaction_window_bars
        
    def generate_labels(self, target_levels: List[Any], dataset: Any) -> List[Label]:
        # Read the CSV to get future bars
        import csv
        bars = []
        with open(dataset, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                bars.append({
                    "timestamp": int(row["timestamp"]),
                    "high": float(row["high"]),
                    "low": float(row["low"]),
                    "close": float(row["close"])
                })
        
        # Create a fast lookup for bar index by timestamp
        ts_to_idx = {b["timestamp"]: i for i, b in enumerate(bars)}
        
        labels = []
        for level in target_levels:
            lvl_ts = level.get("creation_timestamp_ms", 0)
            lvl_price = level.get("price_level", 0.0)
            idx = ts_to_idx.get(lvl_ts, -1)
            
            max_reaction_ticks = 0
            bars_to_reaction = -1
            
            # Look ahead in the window
            if idx != -1:
                end_idx = min(idx + 1 + self.reaction_window_bars, len(bars))
                for i in range(idx + 1, end_idx):
                    future_bar = bars[i]
                    # We assume it's a resistance level (pivot high). Price must go DOWN to react.
                    # Reaction size = Level Price - lowest low in the window before it breaks the level
                    
                    if future_bar["high"] > lvl_price:
                        # Level broken
                        break
                        
                    reaction = (lvl_price - future_bar["low"]) / 0.1 # assuming 1 tick = 0.1 for BTC
                    if reaction > max_reaction_ticks:
                        max_reaction_ticks = reaction
                        bars_to_reaction = i - idx
                        
            observed_facts = {
                "max_reaction_ticks": max_reaction_ticks,
                "bars_to_reaction": bars_to_reaction,
                "was_broken_immediately": (bars_to_reaction == -1)
            }
            
            # Map observed facts to Derived Class
            if max_reaction_ticks >= self.reaction_ticks and bars_to_reaction <= self.reaction_window_bars:
                derived_class = "POSITIVE"
                reason = f"Reaction {max_reaction_ticks} >= {self.reaction_ticks}"
            else:
                derived_class = "NEGATIVE"
                reason = "Insufficient reaction within window"
                
            target_id = level.get("uuid", "unknown")
            labels.append(Label(
                label_id=f"LBL-{target_id}-001",
                target_object_id=target_id,
                dataset_version="ENG-SYN-0001",
                dataset_hash="0c7e2d630be68e06",
                configuration_hash="CFG-0001-HASH",
                schema_version="v1.0",
                generator_version=self.generator_version,
                policy_version=self.policy_version,
                generation_timestamp_ms=1700000000,
                generator_commit="a1b2c3d",
                observed_facts=observed_facts,
                derived_class=derived_class,
                confidence=1.0,
                lookahead_window_bars=self.reaction_window_bars,
                reason=reason
            ))
            
        return labels
