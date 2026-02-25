#!/usr/bin/env python3
import curses
import os
import signal

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PID_DIR = os.path.join(PROJECT_ROOT, "pids")

COMPONENTS = [
    "Web Dashboard",
    "TUI Dashboard",
    "SSRF Scanner",
    "Manager",
]

def pid_file_for(name: str) -> str:
    safe = name.lower().replace(" ", "_")
    return os.path.join(PID_DIR, f"{safe}.pid")

def is_running(name: str) -> tuple[bool, str]:
    pf = pid_file_for(name)
    if not os.path.exists(pf):
        return False, "no PID file"
    try:
        with open(pf) as f:
            pid = int(f.read().strip())
    except Exception:
        return False, "invalid PID file"
    try:
        os.kill(pid, 0)
        return True, f"PID {pid}"
    except ProcessLookupError:
        return False, f"stale PID {pid}"

def draw(stdscr):
    curses.curs_set(0)
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "SSRF Console Health Dashboard (q=quit)")
        for i, name in enumerate(COMPONENTS):
            running, info = is_running(name)
            status = "UP  " if running else "DOWN"
            color = curses.color_pair(1 if running else 2)
            stdscr.addstr(2 + i, 0, f"{name:15} ", curses.A_BOLD)
            stdscr.addstr(f"{status} ", color)
            stdscr.addstr(f"({info})")
        stdscr.refresh()
        ch = stdscr.getch()
        if ch == ord("q"):
            break

def main():
    curses.wrapper(init)

def init(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    draw(stdscr)

if __name__ == "__main__":
    main()
