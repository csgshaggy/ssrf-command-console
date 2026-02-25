from fastapi import APIRouter, HTTPException, Depends
from app.auth_rbac import require_role
import os

router = APIRouter(
    prefix="/logs",
    tags=["logs"],
    dependencies=[Depends(require_role("admin"))],  # admin-only
)

LOG_DIR = "/app/logs"


# ------------------------------------------------------------
# List available log files
# ------------------------------------------------------------
@router.get("/", summary="List available log files")
def list_logs():
    if not os.path.exists(LOG_DIR):
        raise HTTPException(status_code=404, detail="Log directory not found")

    files = [
        f for f in os.listdir(LOG_DIR)
        if f.endswith(".log")
    ]

    return {"logs": files}


# ------------------------------------------------------------
# Read a specific log file
# ------------------------------------------------------------
@router.get("/{log_name}", summary="Read a specific log file")
def read_log(log_name: str):
    path = os.path.join(LOG_DIR, log_name)

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Log file not found")

    with open(path, "r") as f:
        content = f.read()

    return {
        "log": log_name,
        "content": content,
    }
