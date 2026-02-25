import subprocess
from pathlib import Path

# ------------------------------------------------------------
# Project Paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
LOGS_DIR = PROJECT_ROOT / "logs"

LOGS_DIR.mkdir(exist_ok=True)


def _run_script(script_name: str):
    """
    Execute a script from the scripts/ directory.
    """
    script_path = SCRIPTS_DIR / script_name

    if not script_path.exists():
        print(f"[ERROR] Script not found: {script_path}")
        return

    try:
        subprocess.run(["bash", str(script_path)], check=False)
    except Exception as e:
        print(f"[ERROR] Failed to run {script_name}: {e}")


# ------------------------------------------------------------
# Backend Control Functions
# ------------------------------------------------------------

def kill_backend():
    print("[*] Killing backend on port 8000...")
    _run_script("kill_port.sh")


def kill_and_restart_backend():
    print("[*] Killing and restarting backend...")
    _run_script("kill_and_restart.sh")


def kill_multi_ports():
    print("[*] Killing multiple ports...")
    _run_script("kill_ports.sh")


def start_backend_direct():
    print("[*] Starting backend directly (uvicorn app.main:app --reload)...")
    try:
        subprocess.Popen(
            ["uvicorn", "app.main:app", "--reload"],
            cwd=str(PROJECT_ROOT)
        )
    except Exception as e:
        print(f"[ERROR] Failed to start backend: {e}")


def backend_status():
    """
    Check if backend is running on port 8000.
    """
    try:
        result = subprocess.run(
            ["lsof", "-t", "-i", ":8000"],
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            print(f"[+] Backend running. PIDs: {result.stdout.strip()}")
        else:
            print("[-] Backend is NOT running.")
    except Exception as e:
        print(f"[ERROR] Failed to check backend status: {e}")
