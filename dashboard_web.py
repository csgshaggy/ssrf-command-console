import os
import subprocess
import time

from fastapi import FastAPI
from pydantic import BaseModel

from ssrf_scanner.parallel_scan import scan_ips_parallel
from ssrf_scanner.dashboard_formatter import summarize_ip_result

PROJECT_ROOT = os.path.expanduser("~/SSRF_CONSOLE")
BACKEND_PORT = 5001

app = FastAPI()


class ScanRequest(BaseModel):
    ips: list[str]
    workers: int = 10


def run_cmd(cmd: str) -> str:
    return subprocess.getoutput(cmd)


# ============================
# Core API
# ============================

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/scan")
def run_scan(req: ScanRequest):
    results = scan_ips_parallel(req.ips, max_workers=req.workers)

    summaries = {}
    for ip, result in results.items():
        if "error" in result:
            summaries[ip] = {"ip": ip, "error": result["error"]}
            continue
        summaries[ip] = summarize_ip_result(result)

    return {"results": results, "summaries": summaries}


# ============================
# Control Panel API
# ============================

@app.get("/control/health")
def control_health():
    return {"health": "ok"}


@app.get("/control/ports")
def control_ports():
    backend = run_cmd(f"ss -tulpn | grep {BACKEND_PORT}")
    frontend = run_cmd("ss -tulpn | grep 8000")
    return {
        "backend_port": backend or "free",
        "frontend_port": frontend or "free",
    }


@app.get("/control/processes")
def control_processes():
    procs = run_cmd("ps aux | grep -E 'uvicorn|http.server|python3' | grep -v grep")
    return {"processes": procs or "none"}


@app.post("/control/manual_scan")
def control_manual_scan():
    results = scan_ips_parallel(["127.0.0.1"], max_workers=5)
    return {"results": results}


@app.get("/control/logs")
def control_logs():
    logs = run_cmd("journalctl -u uvicorn --no-pager -n 100")
    if not logs.strip():
        logs = "No uvicorn logs found. If uvicorn is not a systemd service, adjust this command."
    return {"logs": logs}


@app.post("/control/restart_backend")
def control_restart_backend():
    """
    Restart uvicorn from inside uvicorn.
    The request will be cut off — this is expected.
    """
    subprocess.Popen(["pkill", "-f", "uvicorn"])

    subprocess.Popen(
        f"cd {PROJECT_ROOT} && "
        f"source venv/bin/activate && "
        f"uvicorn dashboard_web:app --host 0.0.0.0 --port {BACKEND_PORT} --reload",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return {"status": "restarting"}

# -------------------------------------------------
# WebSocket for Live Scan Updates
# -------------------------------------------------

from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws/scan")
async def ws_scan(websocket: WebSocket):
    await websocket.accept()
    try:
        # Expect a JSON message: {"ips": [...], "workers": 10}
        data = await websocket.receive_json()
        ips = data.get("ips", [])
        workers = data.get("workers", 10)

        # Notify client that scan is starting
        await websocket.send_json({
            "event": "started",
            "ips": ips,
            "workers": workers
        })

        # Run scan
        results = scan_ips_parallel(ips, max_workers=workers)

        # Summaries
        summaries = {}
        for ip, result in results.items():
            if "error" in result:
                summaries[ip] = {"ip": ip, "error": result["error"]}
            else:
                summaries[ip] = summarize_ip_result(result)

        # Send final results
        await websocket.send_json({
            "event": "finished",
            "results": results,
            "summaries": summaries
        })

        await websocket.close()

    except WebSocketDisconnect:
        return

    except Exception as e:
        await websocket.send_json({
            "event": "error",
            "error": str(e)
        })
        await websocket.close()


# ============================
# Proper Uvicorn Entrypoint
# ============================

if __name__ == "__main__":
    import uvicorn
    from datetime import datetime, UTC

    print(f"[{datetime.now(UTC).isoformat()}] Starting Web Dashboard on port {BACKEND_PORT}")

    uvicorn.run(
        "dashboard_web:app",
        host="0.0.0.0",
        port=BACKEND_PORT,
        reload=False
    )
