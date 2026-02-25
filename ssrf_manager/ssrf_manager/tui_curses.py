import curses
import time
import psutil
import subprocess
from pathlib import Path

from .backend_service import (
    kill_backend,
    kill_and_restart_backend,
    kill_multi_ports,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOGS_DIR = PROJECT_ROOT / "logs"


def get_backend_status():
    result = subprocess.run(
        ["lsof", "-t", "-i", ":8000"],
        capture_output=True,
        text=True,
    )
    pids = result.stdout.strip()
    return bool(pids), pids or None


def get_ports():
    ports = [8000, 8001, 8080, 5000]
    status = {}
    for port in ports:
        res = subprocess.run(
            ["lsof", "-t", "-i", f":{port}"],
            capture_output=True,
            text=True,
        )
        p = res.stdout.strip()
        status[port] = p if p else None
    return status


def get_log_tail(lines=10):
    log_file = LOGS_DIR / "kill_port.log"
    if not log_file.exists():
        return ["No log file found."]
    with log_file.open("r") as f:
        content = f.readlines()
    return [l.rstrip() for l in content[-lines:]] or ["<empty>"]


def draw_panel(win, y, x, h, w, title):
    win.border()
    win.addstr(0, 2, f" {title} ")


def dashboard(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(500)

    while True:
        stdscr.erase()
        max_y, max_x = stdscr.getmaxyx()

        # Layout
        top_h = max_y // 3
        mid_h = max_y // 3
        bot_h = max_y - top_h - mid_h

        # Windows
        backend_win = curses.newwin(top_h, max_x // 2, 0, 0)
        system_win = curses.newwin(top_h, max_x - max_x // 2, 0, max_x // 2)

        ports_win = curses.newwin(mid_h, max_x // 2, top_h, 0)
        proc_win = curses.newwin(mid_h, max_x - max_x // 2, top_h, max_x // 2)

        logs_win = curses.newwin(bot_h, max_x, top_h + mid_h, 0)

        # Data
        backend_running, backend_pids = get_backend_status()
        cpu = psutil.cpu_percent(interval=0.1)
        mem = psutil.virtual_memory()
        load = psutil.getloadavg()
        ports = get_ports()
        log_lines = get_log_tail( bot_h - 4 )

        uvicorn_count = 0
        python_count = 0
        for proc in psutil.process_iter(["name"]):
            name = proc.info["name"] or ""
            if "uvicorn" in name:
                uvicorn_count += 1
            if "python" in name:
                python_count += 1

        # Backend panel
        draw_panel(backend_win, 0, 0, top_h, max_x // 2, "Backend")
        if backend_running:
            backend_win.addstr(2, 2, "Status: RUNNING")
            backend_win.addstr(3, 2, f"PIDs:   {backend_pids}")
        else:
            backend_win.addstr(2, 2, "Status: NOT RUNNING")

        backend_win.addstr(top_h - 3, 2, "[k] Kill  [r] Kill+Restart  [m] Kill Multi")

        # System panel
        draw_panel(system_win, 0, 0, top_h, max_x - max_x // 2, "System")
        system_win.addstr(2, 2, f"CPU:   {cpu:.1f}%")
        system_win.addstr(3, 2, f"RAM:   {mem.percent:.1f}% ({mem.used // (1024**2)}MB / {mem.total // (1024**2)}MB)")
        system_win.addstr(4, 2, f"Load:  {load[0]:.2f}, {load[1]:.2f}, {load[2]:.2f}")

        # Ports panel
        draw_panel(ports_win, 0, 0, mid_h, max_x // 2, "Ports")
        row = 2
        for port, pid in ports.items():
            if pid:
                ports_win.addstr(row, 2, f"{port}: IN USE (PID {pid})")
            else:
                ports_win.addstr(row, 2, f"{port}: free")
            row += 1

        # Process summary panel
        draw_panel(proc_win, 0, 0, mid_h, max_x - max_x // 2, "Processes")
        proc_win.addstr(2, 2, f"Uvicorn processes: {uvicorn_count}")
        proc_win.addstr(3, 2, f"Python processes:  {python_count}")

        # Logs panel
        draw_panel(logs_win, 0, 0, bot_h, max_x, "Last Log Lines")
        row = 2
        for line in log_lines:
            if row < bot_h - 1:
                logs_win.addstr(row, 2, line[: max_x - 4])
                row += 1

        # Footer
        stdscr.addstr(max_y - 1, 2, "[q] Quit  [k] Kill  [r] Kill+Restart  [m] Kill Multi")

        # Refresh
        backend_win.noutrefresh()
        system_win.noutrefresh()
        ports_win.noutrefresh()
        proc_win.noutrefresh()
        logs_win.noutrefresh()
        stdscr.noutrefresh()
        curses.doupdate()

        # Input
        try:
            ch = stdscr.getch()
        except curses.error:
            ch = -1

        if ch == ord("q"):
            break
        elif ch == ord("k"):
            kill_backend()
        elif ch == ord("r"):
            kill_and_restart_backend()
        elif ch == ord("m"):
            kill_multi_ports()

        time.sleep(0.3)


def run():
    curses.wrapper(dashboard)
