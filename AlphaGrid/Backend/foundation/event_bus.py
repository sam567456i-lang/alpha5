"""In-process event bus following the approved event envelope contract."""

from __future__ import annotations

import asyncio
import threading
from collections import defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from inspect import isawaitable
from types import MappingProxyType
from typing import Any, Callable, Mapping
from uuid import uuid4

from .exceptions import EventBusError

EventPayload = Mapping[str, Any]
EventHandler = Callable[["EventEnvelope"], object]


@dataclass(frozen=True, slots=True)
class EventEnvelope:
    """Immutable event envelope defined by the implementation contracts."""

    event_id: str
    event_type: str
    event_version: int
    timestamp: str
    producer: str
    correlation_id: str
    causation_id: str
    payload: EventPayload = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        event_type: str,
        producer: str,
        payload: Mapping[str, Any] | None = None,
        event_version: int = 1,
        correlation_id: str | None = None,
        causation_id: str | None = None,
    ) -> "EventEnvelope":
        """Create a validated immutable event envelope."""

        if event_type.strip() == "":
            raise EventBusError("event_type must not be empty.")
        if producer.strip() == "":
            raise EventBusError("producer must not be empty.")
        if event_version < 1:
            raise EventBusError("event_version must be at least 1.")

        event_id = str(uuid4())
        immutable_payload = MappingProxyType(deepcopy(dict(payload or {})))
        return cls(
            event_id=event_id,
            event_type=event_type,
            event_version=event_version,
            timestamp=datetime.now(tz=timezone.utc).isoformat(),
            producer=producer,
            correlation_id=correlation_id or event_id,
            causation_id=causation_id or event_id,
            payload=immutable_payload,
        )

    def as_dict(self) -> dict[str, Any]:
        """Return a serializable event representation."""

        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "event_version": self.event_version,
            "timestamp": self.timestamp,
            "producer": self.producer,
            "correlation_id": self.correlation_id,
            "causation_id": self.causation_id,
            "payload": dict(self.payload),
        }


class EventBus:
    """Async-safe in-process event bus for foundation-level communication."""

    def __init__(self) -> None:
        self._subscribers: dict[str, list[EventHandler]] = defaultdict(list)
        self._history: deque[EventEnvelope] = deque(maxlen=10_000)
        self._lock = asyncio.Lock()
        self._sub_lock = threading.Lock()

    async def publish(self, event: EventEnvelope) -> None:
        """Publish an event to exact-match and wildcard subscribers."""

        handlers = await self._handlers_for(event.event_type)
        errors: list[BaseException] = []
        for handler in handlers:
            try:
                result = handler(event)
                if isawaitable(result):
                    await result
            except BaseException as exc:
                errors.append(exc)

        async with self._lock:
            self._history.append(event)

        if errors:
            raise EventBusError(
                f"{len(errors)} handler(s) failed for event {event.event_type!r}."
            ) from errors[0]

    async def emit(
        self,
        *,
        event_type: str,
        producer: str,
        payload: Mapping[str, Any] | None = None,
        event_version: int = 1,
        correlation_id: str | None = None,
        causation_id: str | None = None,
    ) -> EventEnvelope:
        """Create, publish, and return an event envelope."""

        event = EventEnvelope.create(
            event_type=event_type,
            producer=producer,
            payload=payload,
            event_version=event_version,
            correlation_id=correlation_id,
            causation_id=causation_id,
        )
        await self.publish(event)
        return event

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """Subscribe a handler to an event type or ``*`` wildcard."""

        if event_type.strip() == "":
            raise EventBusError("event_type must not be empty.")
        if not callable(handler):
            raise EventBusError("handler must be callable.")
        
        # This synchronization strategy is an accepted engineering tradeoff.
        # Acquiring a threading.Lock from async code may briefly block the event loop under contention.
        # This design was chosen because subscriber mutations originate from synchronous contexts while handler dispatch occurs asynchronously.
        # This does NOT eliminate blocking risk.
        with self._sub_lock:
            self._subscribers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: EventHandler) -> None:
        """Remove a previously registered event handler."""

        # This synchronization strategy is an accepted engineering tradeoff.
        # Acquiring a threading.Lock from async code may briefly block the event loop under contention.
        # This design was chosen because subscriber mutations originate from synchronous contexts while handler dispatch occurs asynchronously.
        # This does NOT eliminate blocking risk.
        with self._sub_lock:
            handlers = self._subscribers.get(event_type)
            if not handlers or handler not in handlers:
                raise EventBusError("handler is not subscribed to event type.")
            handlers.remove(handler)

    async def replay(self, event_type: str | None = None) -> None:
        """Replay recorded events using their original envelope versions."""

        async with self._lock:
            events = tuple(self._history)
        for event in events:
            if event_type is None or event.event_type == event_type:
                handlers = await self._handlers_for(event.event_type)
                for handler in handlers:
                    result = handler(event)
                    if isawaitable(result):
                        await result

    async def history(self) -> tuple[EventEnvelope, ...]:
        """Return recorded events."""

        async with self._lock:
            return tuple(self._history)

    async def _handlers_for(self, event_type: str) -> tuple[EventHandler, ...]:
        # This synchronization strategy is an accepted engineering tradeoff.
        # Acquiring a threading.Lock from async code may briefly block the event loop under contention.
        # This design was chosen because subscriber mutations originate from synchronous contexts while handler dispatch occurs asynchronously.
        # This does NOT eliminate blocking risk.
        with self._sub_lock:
            return tuple(self._subscribers.get(event_type, ())) + tuple(
                self._subscribers.get("*", ())
            )
