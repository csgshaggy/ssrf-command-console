import curses

HELP_TEXT = [
    "SSRF Console TUI Help",
    "",
    "Keybindings:",
    "  ↑/↓/PgUp/PgDn  - Scroll output",
    "  P              - Command palette",
    "  h              - Help",
    "  H              - History",
    "  F              - Favorites",
    "  D              - Diagnostics",
    "  T              - Theme",
    "  M              - Output mode",
    "  L              - Layout",
    "  c              - Clear output",
    "  q              - Quit",
    "",
    "Press any key to return..."
]


def draw_help(screen):
    screen.clear()
    h, w = screen.getmaxyx()

    for i, line in enumerate(HELP_TEXT):
        x = 2
        y = 2 + i
        if y < h:
            screen.addstr(y, x, line)

    screen.refresh()
    screen.getch()
