"""WebSocket connection hub — manages all client connections by channel."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from fastapi import WebSocket


class Channel(StrEnum):
    """Supported real-time WebSocket channels."""

    MARKET = "market"
    RECOMMENDATIONS = "recommendations"
    PORTFOLIO = "portfolio"
    AI = "ai"
    NEWS = "news"
    SYSTEM = "system"


class ConnectionHub:
    """Central registry of all active WebSocket client connections.

    Each channel maintains an independent set of connected clients.
    A broadcast on one channel does not affect other channels.
    """

    def __init__(self) -> None:
        self._connections: dict[Channel, set[WebSocket]] = {
            channel: set() for channel in Channel
        }

    async def connect(self, channel: Channel, websocket: WebSocket) -> None:
        """Accept a new WebSocket connection and register it on the given channel."""
        await websocket.accept()
        self._connections[channel].add(websocket)

    def disconnect(self, channel: Channel, websocket: WebSocket) -> None:
        """Remove a WebSocket connection from the given channel."""
        self._connections[channel].discard(websocket)

    async def broadcast(
        self,
        channel: Channel,
        event_type: str,
        payload: Any = None,
    ) -> None:
        """Broadcast a typed JSON event to every connected client on a channel.

        Clients that have already disconnected are silently removed.
        """
        if not self._connections[channel]:
            return

        message = {"event": event_type, "data": payload}
        dead: list[WebSocket] = []

        for websocket in list(self._connections[channel]):
            try:
                await websocket.send_json(message)
            except Exception:
                dead.append(websocket)

        for websocket in dead:
            self.disconnect(channel, websocket)

    def connection_count(self, channel: Channel) -> int:
        """Return the number of active connections on a given channel."""
        return len(self._connections[channel])


# Module-level singleton shared across the entire application lifetime.
hub = ConnectionHub()
