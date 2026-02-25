from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from typing import Dict, Any
from pathlib import Path

from app.health import (
    get_system_stats,
    get_system_deep,
    get_backend_status,
    get_ports_status,
    get_top_processes,
)
from app.logs_api import tail_lines

router = APIRouter()

LOG_FILE = Path("logs/backend.log")
AUDIT_LOG_FILE = Path("logs/audit.log")


async def build_dashboard_payload() -> Dict[str, Any]:
    system = get_system_stats()
    system_deep = get_system_deep()
    backend = get_backend_status()
    ports = get_ports_status([8000, 8001, 6379])
    process_top = get_top_processes(limit=5)
    logs = tail_lines(LOG_FILE, n=50)
    audit = tail_lines(AUDIT_LOG_FILE, n=50)

    return {
        "system": system,
        "system_deep": system_deep,
        "backend": backend,
        "ports": ports,
        "process_top": process_top,
        "logs": logs,
        "audit": audit,
    }


@router.websocket("/ws/dashboard")
async def dashboard_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            payload = await build_dashboard_payload()
            await websocket.send_json(payload)
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        pass
    except Exception:
        # Optional: log error somewhere
        pass
