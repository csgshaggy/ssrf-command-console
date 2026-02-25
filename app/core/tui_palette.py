import curses

# Color name → (fg, bg)
PALETTE = {
    "header": (curses.COLOR_BLACK, curses.COLOR_CYAN),
    "footer": (curses.COLOR_BLACK, curses.COLOR_BLUE),
    "status": (curses.COLOR_BLACK, curses.COLOR_MAGENTA),
    "sidebar": (curses.COLOR_YELLOW, curses.COLOR_BLACK),
    "output": (curses.COLOR_WHITE, curses.COLOR_BLACK),
}

COLOR_PAIRS = {}


def init_colors():
    """Initialize curses color pairs."""
    if not curses.has_colors():
        return

    curses.start_color()

    pair_id = 1
    for name, (fg, bg) in PALETTE.items():
        curses.init_pair(pair_id, fg, bg)
        COLOR_PAIRS[name] = curses.color_pair(pair_id)
        pair_id += 1


def get_color_pair(name: str):
    """Return a curses color pair, or 0 if missing."""
    return COLOR_PAIRS.get(name, 0)
