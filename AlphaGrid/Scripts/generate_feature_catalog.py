import os
import sys
import importlib
import inspect

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from Backend.features.interfaces.momentum_feature import MomentumFeatureInterface
from Backend.features.interfaces.trend_feature import TrendFeatureInterface
from Backend.features.interfaces.volatility_feature import VolatilityFeatureInterface

def discover_features():
    features_dir = os.path.join(project_root, "Backend", "features")
    sys.path.insert(0, features_dir)
    
    feature_classes = []
    
    for filename in os.listdir(features_dir):
        if filename.endswith("_generator.py"):
            module_name = filename[:-3]
            try:
                module = importlib.import_module(f"Backend.features.{module_name}")
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and obj.__module__ == module.__name__:
                        # Check if it implements one of the interfaces
                        if issubclass(obj, (MomentumFeatureInterface, TrendFeatureInterface, VolatilityFeatureInterface)):
                            if name != "MomentumFeatureInterface" and name != "TrendFeatureInterface" and name != "VolatilityFeatureInterface":
                                feature_classes.append(obj)
            except Exception as e:
                print(f"Failed to load {module_name}: {e}")
                
    return feature_classes

def generate_catalog():
    docs_dir = os.path.join(project_root, "Docs", "Architecture")
    os.makedirs(docs_dir, exist_ok=True)
    out_path = os.path.join(docs_dir, "feature_catalog.md")
    
    classes = discover_features()
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# AlphaGrid Feature Catalog\n\n")
        f.write("This catalog is auto-generated from the Feature Generator components.\n\n")
        
        f.write("| Feature Generator | Component ID Format | Interface | Dependencies |\n")
        f.write("|---|---|---|---|\n")
        
        for cls in sorted(classes, key=lambda x: x.__name__):
            # Attempt to instantiate to get metadata (using defaults)
            try:
                # Assuming signature has defaults for all params
                instance = cls()
                comp_id = instance.component_id
                
                # Check which interface it implements
                interface = "Unknown"
                if issubclass(cls, MomentumFeatureInterface): interface = "MomentumFeatureInterface"
                elif issubclass(cls, TrendFeatureInterface): interface = "TrendFeatureInterface"
                elif issubclass(cls, VolatilityFeatureInterface): interface = "VolatilityFeatureInterface"
                
                f.write(f"| `{cls.__name__}` | `{comp_id}` | `{interface}` | `['ftr-ohlcv']` |\n")
            except Exception as e:
                f.write(f"| `{cls.__name__}` | `Unknown (Requires args)` | `Unknown` | `Unknown` |\n")
                
    print(f"Successfully generated Feature Catalog at {out_path}")

if __name__ == "__main__":
    generate_catalog()
