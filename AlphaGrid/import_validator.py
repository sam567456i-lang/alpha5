import importlib
import sys

modules_to_test = [
    'Backend.dtos',
    'Backend.features',
    'Backend.concepts.core',
    'Backend.methodologies',
    'Backend.signals.primitive.generators',
    'Backend.strategy.strategies',
]

success = True
for mod in modules_to_test:
    try:
        importlib.import_module(mod)
        print(f"PASS: {mod}")
    except Exception as e:
        print(f"FAIL: {mod} -> {e}")
        success = False

if not success:
    sys.exit(1)
