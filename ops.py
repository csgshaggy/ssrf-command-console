from fastapi import APIRouter, Depends, HTTPException
import subprocess
import os
from typing import List, Dict, Any

from app.security import require_role

router = APIRouter()


def run_cmd(cmd: List[str]) -> str:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=e.stderr.strip() or "Command failed")


@router.post("/backend/kill")
async def kill_backend(user=Depends(require_role("admin"))):
    """
    Kill backend processes (e.g., uvicorn / python on port 8000).
    Adjust the command to match your environment if needed.
    """
    cmd = ["bash", "-c", "lsof -ti:8000 | xargs -r kill -9"]
    output = run_cmd(cmd)
    return {"status": "ok", "action": "kill_backend", "output": output}


@router.post("/backend/restart")
async def restart_backend(user=Depends(require_role("admin"))):
    """
    Restart backend service via a script.
    Expects scripts/restart_backend.sh to exist and be executable.
    """
    script_path = os.path.join("scripts", "restart_backend.sh")
    if not os.path.exists(script_path):
        raise HTTPException(status_code=500, detail="restart_backend.sh not found")

    cmd = ["bash", script_path]
    output = run_cmd(cmd)
    return {"status": "ok", "action": "restart_backend", "output": output}


@router.post("/backend/kill-multi")
async def kill_multi(user=Depends(require_role("admin"))):
    """
    Kill multiple ports commonly used by the stack.
    Adjust the port list as needed.
    """
    ports = [8000, 8001, 6379]
    outputs: Dict[str, Any] = {}

    for port in ports:
        cmd = ["bash", "-c", f"lsof -ti:{port} | xargs -r kill -9"]
        try:
            outputs[str(port)] = run_cmd(cmd)
        except HTTPException as e:
            outputs[str(port)] = f"error: {e.detail}"

    return {"status": "ok", "action": "kill_multi", "ports": outputs}
