from typing import Dict, Any, Type

class Registry:
    def __init__(self):
        self._items: Dict[str, Any] = {}
        
    def register(self, id: str, item: Any):
        self._items[id] = item
        
    def get(self, id: str) -> Any:
        return self._items.get(id)

class MethodologyRegistry(Registry):
    pass

class ProfileRegistry(Registry):
    pass

class PolicyRegistry(Registry):
    pass

class EvaluatorRegistry(Registry):
    pass

class EvaluationRegistry(Registry):
    pass

class InterpretationRegistry(Registry):
    pass

class ProjectionRegistry(Registry):
    pass
