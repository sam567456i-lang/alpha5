"""Dependency injection and service registry primitives."""

from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from typing import Callable, Generic, TypeVar, cast

from .exceptions import ServiceRegistrationError, ServiceResolutionError

T = TypeVar("T")


@dataclass(slots=True)
class _ServiceRegistration(Generic[T]):
    factory: Callable[["DependencyContainer"], T]
    singleton: bool
    instance: T | None = None


class DependencyContainer:
    """Small dependency container with explicit service registration."""

    def __init__(self) -> None:
        self._registrations: dict[str, _ServiceRegistration[object]] = {}
        self._lock = RLock()

    def register_instance(self, name: str, instance: object) -> None:
        """Register an already-created service instance."""

        self._validate_name(name)
        with self._lock:
            if name in self._registrations:
                raise ServiceRegistrationError(f"Service already registered: {name}")
            self._registrations[name] = _ServiceRegistration(
                factory=lambda _container: instance,
                singleton=True,
                instance=instance,
            )

    def register_factory(
        self,
        name: str,
        factory: Callable[["DependencyContainer"], object],
        *,
        singleton: bool = True,
    ) -> None:
        """Register a service factory."""

        self._validate_name(name)
        with self._lock:
            if name in self._registrations:
                raise ServiceRegistrationError(f"Service already registered: {name}")
            self._registrations[name] = _ServiceRegistration(
                factory=factory,
                singleton=singleton,
            )

    def resolve(self, name: str, expected_type: type[T] | None = None) -> T | object:
        """Resolve a registered service by name."""

        self._validate_name(name)
        with self._lock:
            registration = self._registrations.get(name)
            if registration is None:
                raise ServiceResolutionError(f"Service is not registered: {name}")

            if registration.singleton and registration.instance is not None:
                instance = registration.instance
            else:
                instance = registration.factory(self)
                if registration.singleton:
                    registration.instance = instance

        if expected_type is not None and not isinstance(instance, expected_type):
            raise ServiceResolutionError(
                f"Service {name!r} is not of expected type {expected_type.__name__}."
            )
        return cast(T, instance) if expected_type is not None else instance

    def contains(self, name: str) -> bool:
        """Return whether a service has been registered."""

        self._validate_name(name)
        with self._lock:
            return name in self._registrations

    def registered_names(self) -> tuple[str, ...]:
        """Return registered service names in stable order."""

        with self._lock:
            return tuple(sorted(self._registrations))

    def clear(self) -> None:
        """Remove all service registrations."""

        with self._lock:
            self._registrations.clear()

    @staticmethod
    def _validate_name(name: str) -> None:
        if name.strip() == "":
            raise ServiceRegistrationError("Service name must not be empty.")


ServiceRegistry = DependencyContainer
