"""Application lifecycle orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from inspect import isawaitable
import logging
from typing import Callable

from .exceptions import LifecycleError

LifecycleCallback = Callable[[], object]


class LifecycleState(StrEnum):
    """Application lifecycle states managed by the foundation module."""

    CREATED = "created"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class LifecycleStep:
    """Named lifecycle callback."""

    name: str
    callback: LifecycleCallback


class LifecycleManager:
    """Run startup and shutdown hooks in deterministic order."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        self._startup_steps: list[LifecycleStep] = []
        self._shutdown_steps: list[LifecycleStep] = []
        self._state = LifecycleState.CREATED
        self._logger = logger or logging.getLogger(__name__)

    @property
    def state(self) -> LifecycleState:
        """Return the current lifecycle state."""

        return self._state

    def register_startup(self, name: str, callback: LifecycleCallback) -> None:
        """Register a startup callback."""

        self._register(self._startup_steps, name, callback)

    def register_shutdown(self, name: str, callback: LifecycleCallback) -> None:
        """Register a shutdown callback."""

        self._register(self._shutdown_steps, name, callback)

    async def startup(self) -> None:
        """Run startup callbacks in registration order."""

        if self._state not in {LifecycleState.CREATED, LifecycleState.STOPPED}:
            raise LifecycleError(f"Cannot start from state: {self._state.value}")
        self._state = LifecycleState.STARTING
        self._logger.info("AlphaGrid startup started")
        try:
            for step in self._startup_steps:
                await self._run_step(step)
            self._state = LifecycleState.RUNNING
            self._logger.info("AlphaGrid startup completed")
        except Exception:
            self._state = LifecycleState.FAILED
            self._logger.exception("AlphaGrid startup failed")
            raise

    async def shutdown(self) -> None:
        """Run shutdown callbacks in reverse registration order."""

        if self._state in {LifecycleState.STOPPING, LifecycleState.STOPPED}:
            return
        self._state = LifecycleState.STOPPING
        self._logger.info("AlphaGrid shutdown started")
        errors: list[BaseException] = []
        for step in reversed(self._shutdown_steps):
            try:
                await self._run_step(step)
            except BaseException as exc:
                errors.append(exc)
                self._logger.exception("AlphaGrid shutdown step failed")
        self._state = LifecycleState.STOPPED if not errors else LifecycleState.FAILED
        self._logger.info("AlphaGrid shutdown completed")
        if errors:
            raise LifecycleError(
                f"{len(errors)} shutdown step(s) failed."
            ) from errors[0]

    def startup_step_names(self) -> tuple[str, ...]:
        """Return registered startup step names."""

        return tuple(step.name for step in self._startup_steps)

    def shutdown_step_names(self) -> tuple[str, ...]:
        """Return registered shutdown step names."""

        return tuple(step.name for step in self._shutdown_steps)

    @staticmethod
    def _register(
        steps: list[LifecycleStep],
        name: str,
        callback: LifecycleCallback,
    ) -> None:
        if name.strip() == "":
            raise LifecycleError("Lifecycle step name must not be empty.")
        if not callable(callback):
            raise LifecycleError("Lifecycle callback must be callable.")
        if any(step.name == name for step in steps):
            raise LifecycleError(f"Lifecycle step already registered: {name}")
        steps.append(LifecycleStep(name=name, callback=callback))

    @staticmethod
    async def _run_step(step: LifecycleStep) -> None:
        result = step.callback()
        if isawaitable(result):
            await result
