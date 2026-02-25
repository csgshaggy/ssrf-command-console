from fastapi import APIRouter
import psutil
import socket
import time

router = APIRouter(
    prefix="/health",
    tags=["health"],
)

# ------------------------------------------------------------
# Basic health check
# ------------------------------------------------------------
@router.get("/", summary="Basic health check")
def health_root():
    return {
        "status": "ok",
        "timestamp": time.time(),
    }

# ------------------------------------------------------------
# System resource health
# ------------------------------------------------------------
@router.get("/system", summary="System resource health")
def system_health():
    cpu = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    return {
        "cpu_percent": cpu,
        "memory_percent": memory,
        "disk_percent": disk,
        "timestamp": time.time(),
    }

# ------------------------------------------------------------
# List open TCP ports
# ------------------------------------------------------------
@router.get("/ports", summary="List open TCP ports")
def list_open_ports():
    connections = psutil.net_connections(kind="tcp")
    open_ports = sorted({
        conn.laddr.port
        for conn in connections
        if conn.status == "LISTEN"
    })

    return {
        "open_ports": open_ports,
        "count": len(open_ports),
        "timestamp": time.time(),
    }

# ------------------------------------------------------------
# Hostname + IP info
# ------------------------------------------------------------
@router.get("/hostname", summary="Return hostname and IP")
def hostname_info():
    hostname = socket.gethostname()

    try:
        ip = socket.gethostbyname(hostname)
    except Exception:
        ip = "unknown"

    return {
        "hostname": hostname,
        "ip": ip,
        "timestamp": time.time(),
    }
