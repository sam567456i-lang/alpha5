import inspect
import json
import logging
from typing import Any, Callable, Dict, List, Set, Tuple
from unittest.mock import patch

from Backend.foundation.dependency_injection_container import DependencyContainer
from Backend.foundation.event_bus import EventBus
from Backend.foundation.base_registry import BaseRegistry

logger = logging.getLogger("RuntimeAuditor.Instrumentation")

class InstrumentationContext:
    """Singleton context to hold runtime tracking data."""
    di_registrations: List[Dict[str, Any]] = []
    di_resolutions: List[Dict[str, Any]] = []
    event_subscriptions: List[Dict[str, Any]] = []
    event_publications: List[Dict[str, Any]] = []
    registry_writes: List[Dict[str, Any]] = []
    registry_reads: List[Dict[str, Any]] = []

    @classmethod
    def reset(cls):
        cls.di_registrations.clear()
        cls.di_resolutions.clear()
        cls.event_subscriptions.clear()
        cls.event_publications.clear()
        cls.registry_writes.clear()
        cls.registry_reads.clear()

    @classmethod
    def dump_to_disk(cls, output_dir: str):
        import os
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "di_graph.json"), "w") as f:
            json.dump({"registrations": cls.di_registrations, "resolutions": cls.di_resolutions}, f, indent=2, default=str)
        with open(os.path.join(output_dir, "event_graph.json"), "w") as f:
            json.dump({"subscriptions": cls.event_subscriptions, "publications": cls.event_publications}, f, indent=2, default=str)
        with open(os.path.join(output_dir, "registry_graph.json"), "w") as f:
            json.dump({"writes": cls.registry_writes, "reads": cls.registry_reads}, f, indent=2, default=str)


def _get_caller_info() -> str:
    """Helper to extract the exact module calling the instrumented function."""
    stack = inspect.stack()
    # Find the first frame outside this file and outside foundation modules
    for frame_info in stack:
        module = inspect.getmodule(frame_info[0])
        if module:
            module_name = module.__name__
            if "runtime_auditor" not in module_name and "unittest.mock" not in module_name and "Backend.foundation" not in module_name:
                return module_name
    return "unknown"


# --- DI Container Instrumentation ---
_orig_register_instance = DependencyContainer.register_instance
_orig_register_factory = DependencyContainer.register_factory
_orig_resolve = DependencyContainer.resolve

def _hook_register_instance(self, name: str, instance: object) -> None:
    caller = _get_caller_info()
    InstrumentationContext.di_registrations.append({
        "name": name,
        "type": "instance",
        "instance_class": instance.__class__.__name__,
        "caller": caller
    })
    return _orig_register_instance(self, name, instance)

def _hook_register_factory(self, name: str, factory: Callable, *, singleton: bool = True) -> None:
    caller = _get_caller_info()
    InstrumentationContext.di_registrations.append({
        "name": name,
        "type": "factory",
        "singleton": singleton,
        "caller": caller
    })
    return _orig_register_factory(self, name, factory, singleton=singleton)

def _hook_resolve(self, name: str, expected_type=None) -> Any:
    caller = _get_caller_info()
    InstrumentationContext.di_resolutions.append({
        "name": name,
        "expected_type": expected_type.__name__ if expected_type else None,
        "caller": caller
    })
    return _orig_resolve(self, name, expected_type)


# --- Event Bus Instrumentation ---
_orig_subscribe = EventBus.subscribe
_orig_publish = EventBus.publish

def _hook_subscribe(self, event_type: str, handler: Callable) -> None:
    caller = _get_caller_info()
    InstrumentationContext.event_subscriptions.append({
        "event_type": event_type,
        "handler_name": handler.__name__ if hasattr(handler, '__name__') else str(handler),
        "caller": caller
    })
    return _orig_subscribe(self, event_type, handler)

async def _hook_publish(self, event) -> None:
    caller = _get_caller_info()
    InstrumentationContext.event_publications.append({
        "event_type": event.event_type,
        "producer": event.producer,
        "caller": caller
    })
    return await _orig_publish(self, event)


# --- Base Registry Instrumentation ---
_orig_register = BaseRegistry.register
_orig_get = BaseRegistry.get

def _hook_base_register(self, key: str, item: Any) -> None:
    caller = _get_caller_info()
    InstrumentationContext.registry_writes.append({
        "registry_name": self.name,
        "key": key,
        "item_type": item.__class__.__name__,
        "caller": caller
    })
    return _orig_register(self, key, item)

def _hook_base_get(self, key: str) -> Any:
    caller = _get_caller_info()
    InstrumentationContext.registry_reads.append({
        "registry_name": self.name,
        "key": key,
        "caller": caller
    })
    return _orig_get(self, key)


class AuditorInstrumentor:
    """Manages applying and removing architectural monkey-patches."""
    
    def __init__(self):
        self._patches = []

    def apply(self):
        InstrumentationContext.reset()
        
        self._patches.extend([
            patch.object(DependencyContainer, 'register_instance', _hook_register_instance),
            patch.object(DependencyContainer, 'register_factory', _hook_register_factory),
            patch.object(DependencyContainer, 'resolve', _hook_resolve),
            patch.object(EventBus, 'subscribe', _hook_subscribe),
            patch.object(EventBus, 'publish', _hook_publish),
            patch.object(BaseRegistry, 'register', _hook_base_register),
            patch.object(BaseRegistry, 'get', _hook_base_get),
        ])
        
        for p in self._patches:
            p.start()
        
        logger.info("RuntimeAuditor: Core architectural instrumentation applied.")

    def remove(self):
        for p in self._patches:
            p.stop()
        self._patches.clear()
        logger.info("RuntimeAuditor: Core architectural instrumentation removed.")
