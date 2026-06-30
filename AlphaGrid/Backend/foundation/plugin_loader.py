"""Plugin module loading support for foundation services."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from types import ModuleType
from typing import Callable

from .dependency_injection_container import DependencyContainer
from .exceptions import PluginLoadError

PluginRegisterFunction = Callable[[DependencyContainer], object]


@dataclass(frozen=True, slots=True)
class LoadedPlugin:
    """Metadata for a loaded plugin module."""

    module_path: str
    module: ModuleType


class PluginLoader:
    """Load Python plugin modules and invoke optional registration hooks."""

    def __init__(self, container: DependencyContainer) -> None:
        self._container = container
        self._loaded: dict[str, LoadedPlugin] = {}

    def load(self, module_path: str) -> LoadedPlugin:
        """Import a plugin module and call its register hook when present."""

        if module_path.strip() == "":
            raise PluginLoadError("Plugin module path must not be empty.")
        if module_path in self._loaded:
            return self._loaded[module_path]

        try:
            module = import_module(module_path)
        except Exception as exc:
            raise PluginLoadError(f"Could not import plugin: {module_path}") from exc

        register = getattr(module, "register", None)
        if register is not None:
            if not callable(register):
                raise PluginLoadError(
                    f"Plugin register attribute is not callable: {module_path}"
                )
            register(self._container)

        loaded = LoadedPlugin(module_path=module_path, module=module)
        self._loaded[module_path] = loaded
        return loaded

    def loaded_plugins(self) -> tuple[str, ...]:
        """Return loaded plugin module paths."""

        return tuple(sorted(self._loaded))
