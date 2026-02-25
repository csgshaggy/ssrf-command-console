#!/usr/bin/env bash
cd "$(dirname "$0")" || exit 1

PYTHON=python3

$PYTHON - << 'EOF'
import os, sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
PID_DIR = PROJECT_ROOT / "pids"

components = ["Web Dashboard", "TUI Dashboard", "SSRF Scanner", "Manager"]

def pid_file_for(name: str) -> Path:
    safe = name.lower().replace(" ", "_")
    return PID_DIR / f"{safe}.pid"

def check(name: str):
    pf = pid_file_for(name)
    if not pf.exists():
        print(f"[DOWN] {name} (no PID file)")
        return False
    try:
        pid = int(pf.read_text().strip())
    except Exception:
        print(f"[WARN] {name} (invalid PID file)")
        return False
    try:
        os.kill(pid, 0)
        print(f"[UP]   {name} (PID {pid})")
        return True
    except ProcessLookupError:
        print(f"[DOWN] {name} (stale PID {pid})")
        return False

ok = True
for c in components:
    if not check(c):
        ok = False

sys.exit(0 if ok else 1)
EOF
