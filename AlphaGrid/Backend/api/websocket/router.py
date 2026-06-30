"""WebSocket endpoint definitions for all real-time channels."""

from __future__ import annotations

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from .hub import Channel, hub

router = APIRouter(tags=["WebSocket"])


async def _channel_handler(channel: Channel, websocket: WebSocket) -> None:
    """Generic handler: connects a client, keeps the connection alive, and cleans up on disconnect."""
    await hub.connect(channel, websocket)
    try:
        while True:
            # Keep the connection alive; clients may send ping messages.
            await websocket.receive_text()
    except WebSocketDisconnect:
        hub.disconnect(channel, websocket)


@router.websocket("/ws/market")
async def ws_market(websocket: WebSocket) -> None:
    """Real-time market price update channel."""
    await _channel_handler(Channel.MARKET, websocket)


@router.websocket("/ws/recommendations")
async def ws_recommendations(websocket: WebSocket) -> None:
    """Real-time recommendation creation and update channel."""
    await _channel_handler(Channel.RECOMMENDATIONS, websocket)


@router.websocket("/ws/portfolio")
async def ws_portfolio(websocket: WebSocket) -> None:
    """Real-time portfolio state update channel."""
    await _channel_handler(Channel.PORTFOLIO, websocket)


@router.websocket("/ws/ai")
async def ws_ai(websocket: WebSocket) -> None:
    """Real-time AI prediction and result channel."""
    await _channel_handler(Channel.AI, websocket)


@router.websocket("/ws/news")
async def ws_news(websocket: WebSocket) -> None:
    """Real-time market news and alerts channel."""
    await _channel_handler(Channel.NEWS, websocket)


@router.websocket("/ws/system")
async def ws_system(websocket: WebSocket) -> None:
    """Real-time system health and lifecycle event channel."""
    await _channel_handler(Channel.SYSTEM, websocket)
