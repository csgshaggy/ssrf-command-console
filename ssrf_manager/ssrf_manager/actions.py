import subprocess
import time
import os

from .utils import run, color, rotate_log
from .config import get_project_root, get_dashboard_dir, get_venv_activate

def start_backend(cfg):
    print(color("\n🚀 Starting backend...", "blue"))

    log_path = os.path.join(get_project_root(), "backend.log")
    rotate_log(log_path)

    cmd = (
        f"clear && cd {get_project_root()} && "
        f". {get_venv_activate()} && "
        f"uvicorn dashboard_web:app --host 0.0.0.0 --port {cfg.backend_port} --reload "
        f"2>&1 | tee -a {log_path}"
    )

    if cfg.headless:
        subprocess.Popen(["bash", "-c", cmd])
        return

    subprocess.Popen([
        "xfce4-terminal",
        "--disable-server",
        "--hold",
        "--title=Backend Logs",
        "-e",
        f"bash -c '{cmd}'"
    ])

    time.sleep(0.3)
    subprocess.Popen(["wmctrl", "-r", ":ACTIVE:", "-t", "1"])

def start_frontend(cfg):
    print(color("\n🌐 Starting frontend...", "blue"))

    log_path = os.path.join(get_project_root(), "frontend.log")
    rotate_log(log_path)

    cmd = (
        f"clear && cd {get_dashboard_dir()} && "
        f"python3 -m http.server {cfg.frontend_port} "
        f"2>&1 | tee -a {log_path}"
    )

    if cfg.headless:
        subprocess.Popen(["bash", "-c", cmd])
        return

    subprocess.Popen([
        "xfce4-terminal",
        "--disable-server",
        "--hold",
        "--title=Frontend Logs",
        "-e",
        f"bash -c '{cmd}'"
    ])

    time.sleep(0.3)
    subprocess.Popen(["wmctrl", "-r", ":ACTIVE:", "-t", "2"])
    subprocess.Popen(["wmctrl", "-s", "0"])
    subprocess.Popen(["xdg-open", f"http://127.0.0.1:{cfg.frontend_port}"])
