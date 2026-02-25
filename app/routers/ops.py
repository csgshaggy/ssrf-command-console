from fastapi import APIRouter, HTTPException, Depends
from app.auth_rbac import require_role
import subprocess
import os

router = APIRouter(
    prefix="/ops",
    tags=["ops"],
    dependencies=[Depends(require_role("operator"))],  # operator or admin
)

# ------------------------------------------------------------
# Helper: Run a shell command safely
# ------------------------------------------------------------
def run_command(cmd: str):
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        return {
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------------------------------------
# Restart backend service
# ------------------------------------------------------------
@router.post("/restart-backend", summary="Restart backend service")
def restart_backend():
    return run_command("sh /app/scripts/restart_backend.sh")


# ------------------------------------------------------------
# Kill processes on a port
# ------------------------------------------------------------
@router.post("/kill-port/{port}", summary="Kill processes on a port")
def kill_port(port: int):
    return run_command(f"sh /app/scripts/kill_port.sh {port}")


# ------------------------------------------------------------
# Run an arbitrary script from /app/scripts
# ------------------------------------------------------------
@router.post("/run-script", summary="Run an arbitrary script")
def run_script(script_name: str):
    path = f"/app/scripts/{script_name}"

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Script not found")

    return run_command(f"sh {path}")
