import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Backend.research.strategies import register_all_strategies
from Backend.research.strategies.registry import StrategyRegistry
from Backend.features.engine import FeatureEngine
from Backend.features.registry import FeatureRegistry

register_all_strategies()
print("Strategies:", len(StrategyRegistry.get_all()))

f_reg = FeatureRegistry()
for d in StrategyRegistry.get_all():
    print(f"Strategy {d.id} features:", d.features)
    for feat in d.features:
        try:
            f_reg.register(feat)
        except ValueError:
            pass # Duplicate

engine = FeatureEngine(f_reg)
order = engine._feature_instances
print("Features in DAG:", len(order))
