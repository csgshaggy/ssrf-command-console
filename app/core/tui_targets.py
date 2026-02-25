import curses
import os


TARGET_MODES = ["single", "list", "file"]


def draw_target_mode(screen):
    """
    Popup selector for target mode:
    - single: one target
    - list: comma-separated list
    - file: file containing targets
    """
    screen.clear()
    h, w = screen.getmaxyx()

    title = "Select Target Mode"
    screen.addstr(1, (w - len(title)) // 2, title, curses.A_BOLD)

    for i, mode in enumerate(TARGET_MODES):
        y = 3 + i
        x = 4
        screen.addstr(y, x, f"{i+1}. {mode}")

    screen.refresh()

    while True:
        key = screen.getch()
        if key in (ord('1'), ord('2'), ord('3')):
            return TARGET_MODES[key - ord('1')]
        if key == 27:  # ESC
            return "single"


def expand_targets(value: str, mode: str):
    """
    Expand input based on target mode.
    - single: return [value]
    - list: split by comma
    - file: read lines from file
    """
    if mode == "single":
        return [value.strip()]

    if mode == "list":
        return [v.strip() for v in value.split(",") if v.strip()]

    if mode == "file":
        if not os.path.isfile(value):
            return []
        with open(value, "r") as f:
            return [line.strip() for line in f if line.strip()]

    return []
