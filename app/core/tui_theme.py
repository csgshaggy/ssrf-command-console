import curses

THEMES = [
    "default",
    "high_contrast",
    "night",
    "blue",
    "matrix",
]


def draw_theme_selector(screen):
    """Popup window to select a theme name."""
    h, w = screen.getmaxyx()
    win_h = 10
    win_w = 40

    start_y = (h - win_h) // 2
    start_x = (w - win_w) // 2

    win = curses.newwin(win_h, win_w, start_y, start_x)
    win.keypad(True)

    index = 0

    while True:
        win.clear()
        win.border()
        win.addstr(0, 2, " Select Theme ")

        for i, theme in enumerate(THEMES):
            if i == index:
                win.attron(curses.A_REVERSE)
                win.addstr(i + 2, 2, theme)
                win.attroff(curses.A_REVERSE)
            else:
                win.addstr(i + 2, 2, theme)

        win.refresh()
        key = win.getch()

        if key == curses.KEY_UP:
            index = max(0, index - 1)
        elif key == curses.KEY_DOWN:
            index = min(len(THEMES) - 1, index + 1)
        elif key in (10, 13):  # ENTER
            return THEMES[index]
        elif key == 27:  # ESC
            return None
