import asyncio
from typing import Dict, Set
from fastapi import WebSocket


class WebSocketManager:
    """
    Manages active WebSocket connections for the SSRF Command Console.
    Supports:
      - Tracking connected clients
      - Sending messages to one client
      - Broadcasting to all clients
      - Graceful disconnect handling
    """

    def __init__(self):
        # Track active WebSocket connections
        self.active_connections: Set[WebSocket] = set()

        # Optional: track clients by ID if needed later
        self.client_map: Dict[str, WebSocket] = {}

        # Lock to prevent race conditions during broadcast
        self._lock = asyncio.Lock()

    # ------------------------------------------------------------
    # Connection Management
    # ------------------------------------------------------------
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

        # Remove from client_map if present
        for key, ws in list(self.client_map.items()):
            if ws == websocket:
                del self.client_map[key]

    # ------------------------------------------------------------
    # Messaging
    # ------------------------------------------------------------
    async def send_to(self, websocket: WebSocket, message: dict):
        """Send a JSON message to a single WebSocket client."""
        try:
            await websocket.send_json(message)
        except Exception:
            self.disconnect(websocket)

    async def broadcast(self, message: dict):
        """Send a JSON message to all connected WebSocket clients."""
        async with self._lock:
            dead = []
            for ws in self.active_connections:
                try:
                    await ws.send_json(message)
                except Exception:
                    dead.append(ws)

            # Cleanup dead connections
            for ws in dead:
                self.disconnect(ws)


# Global instance used by routers
ws_manager = WebSocketManager()
