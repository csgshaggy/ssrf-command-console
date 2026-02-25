import subprocess
import sys
import traceback
from typing import List, Optional

from app.core.crash_reporter import write_crash_report
from app.core.health_bootstrap import wait_for_dependencies


def launch_tui_dashboard(
    cmd: Optional[List[str]] = None,
    restart_on_exit: bool = False,
) -> int:
    """
    Launches the TUI dashboard as a separate process.
    Optionally restarts it if it exits.
    """
    if cmd is None:
        # Default TUI entrypoint
        cmd = [sys.executable, "scripts/tui_dashboard.py"]

    # Ensure backend dependencies are ready before launching TUI
    wait_for_dependencies()

    while True:
        try:
            print(f"[TUI] Launching TUI dashboard: {' '.join(cmd)}")
            proc = subprocess.Popen(cmd)
            return_code = proc.wait()
            print(f"[TUI] TUI dashboard exited with code {return_code}")

            if not restart_on_exit:
                return return_code

            print("[TUI] Restarting TUI dashboard after exit...")

        except Exception as exc:
            tb = traceback.format_exc()
            write_crash_report(exc, tb, context="tui_launcher.launch_tui_dashboard")
            print("[TUI] TUI launcher encountered an error. See crash report.")
            return 1


if __name__ == "__main__":
    sys.exit(launch_tui_dashboard())
