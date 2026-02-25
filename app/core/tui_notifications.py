import curses
import time
from typing import List, Tuple


class NotificationManager:
    """
    Simple timed notification manager.
    Stores (message, color_pair, expires_at).
    """

    def __init__(self, duration: float = 3.0):
        self.duration = duration
        self._items: List[Tuple[str, int, float]] = []

    def add(self, message: str, color: int = 0):
        expires_at = time.time() + self.duration
        self._items.append((message, color, expires_at))

    def prune(self):
        now = time.time()
        self._items = [(m, c, t) for (m, c, t) in self._items if t > now]

    def current(self):
        self.prune()
        return self._items[-1] if self._items else None


def draw_notification(screen, manager: NotificationManager):
    """
    Draw the most recent active notification as a small popup at the bottom.
    """
    item = manager.current()
    if not item:
        return

    message, color, _ = item
    h, w = screen.getmaxyx()

    win_h = 3
    win_w = min(len(message) + 4, w - 2)
    start_y = h - win_h - 2
    start_x = (w - win_w) // 2

    win = curses.newwin(win_h, win_w, start_y, start_x)
    win.border()

    if color:
        win.attron(curses.color_pair(color))

    win.addstr(1, 2, message[: win_w - 4])

    if color:
        win.attroff(curses.color_pair(color))

    win.refresh()
