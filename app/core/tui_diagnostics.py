import curses
import os
import sys
from app.services.dispatcher_service import dispatcher_service


def gather_diagnostics():
    """
    Collects environment and system diagnostics for display.
    """
    diagnostics = []

    # Working directory
    diagnostics.append(("CWD", os.getcwd()))

    # Python version
    diagnostics.append(("Python", sys.version.split()[0]))

    # Dispatcher health
    try:
        modes = dispatcher_service.list_modes()
        diagnostics.append(("Dispatcher", "OK"))
        diagnostics.append(("Mode Count", str(len(modes))))
    except Exception as e:
        diagnostics.append(("Dispatcher", f"ERROR: {e}"))

    # Template/static directory checks
    diagnostics.append(("Templates Dir", "OK" if os.path.isdir("templates") else "Missing"))
    diagnostics.append(("Static Dir", "OK" if os.path.isdir("static") else "Missing"))

    return diagnostics


def draw_diagnostics(screen):
    """
    Popup window showing system diagnostics.
    """
    data = gather_diagnostics()

    h, w = screen.getmaxyx()
    win_h = min(20, h - 4)
    win_w = min(60, w - 4)

    start_y = (h - win_h) // 2
    start_x = (w - win_w) // 2

    win = curses.newwin(win_h, win_w, start_y, start_x)
    win.keypad(True)
    win.border()

    while True:
        win.clear()
        win.border()
        win.addstr(0, 2, " Diagnostics ")

        for i, (key, value) in enumerate(data):
            line = f"{key}: {value}"
            win.addstr(i + 2, 2, line[: win_w - 4])

        win.refresh()

        key = win.getch()
        if key in (27, ord('q'), ord('D')):
            break
