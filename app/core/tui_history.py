import curses
from datetime import datetime


class HistoryStore:
    """
    Stores past runs for the TUI.
    Each entry is a tuple: (timestamp, mode, target)
    """
    def __init__(self):
        self.entries = []

    def add(self, mode: str, target: str):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.entries.append((ts, mode, target))

    def list(self):
        return self.entries


def draw_history(screen, history: HistoryStore):
    """
    Popup window showing scrollable history.
    """
    entries = history.list()
    if not entries:
        entries = [("No history yet", "", "")]

    h, w = screen.getmaxyx()
    win_h = min(20, h - 4)
    win_w = min(70, w - 4)

    start_y = (h - win_h) // 2
    start_x = (w - win_w) // 2

    win = curses.newwin(win_h, win_w, start_y, start_x)
    win.keypad(True)
    win.border()

    index = 0

    while True:
        win.clear()
        win.border()
        win.addstr(0, 2, " History ")

        # Visible window height
        visible = win_h - 4
        start = max(0, index - visible + 1)
        end = start + visible

        for i, (ts, mode, target) in enumerate(entries[start:end]):
            line = f"{ts} | {mode} | {target}"
            if start + i == index:
                win.attron(curses.A_REVERSE)
                win.addstr(i + 2, 2, line[: win_w - 4])
                win.attroff(curses.A_REVERSE)
            else:
                win.addstr(i + 2, 2, line[: win_w - 4])

        win.refresh()

        key = win.getch()

        if key == curses.KEY_UP:
            index = max(0, index - 1)
        elif key == curses.KEY_DOWN:
            index = min(len(entries) - 1, index + 1)
        elif key in (27, ord('q'), ord('h'), ord('H')):  # ESC, q, h, H closes
            break
