import curses
import difflib


def fuzzy(query, items, limit=10):
    if not query:
        return items[:limit]

    scored = []
    for item in items:
        score = difflib.SequenceMatcher(None, query.lower(), item.lower()).ratio()
        scored.append((score, item))

    scored.sort(reverse=True)
    return [item for score, item in scored[:limit]]


def draw_palette(screen, all_items):
    """Command palette popup."""
    h, w = screen.getmaxyx()
    win_h = 12
    win_w = min(60, w - 4)

    start_y = (h - win_h) // 2
    start_x = (w - win_w) // 2

    win = curses.newwin(win_h, win_w, start_y, start_x)
    win.keypad(True)

    query = ""
    index = 0

    while True:
        win.clear()
        win.border()
        win.addstr(0, 2, " Command Palette ")

        matches = fuzzy(query, all_items)

        win.addstr(1, 2, f"> {query}")

        for i, item in enumerate(matches[: win_h - 4]):
            if i == index:
                win.attron(curses.A_REVERSE)
                win.addstr(i + 3, 2, item[: win_w - 4])
                win.attroff(curses.A_REVERSE)
            else:
                win.addstr(i + 3, 2, item[: win_w - 4])

        win.refresh()
        key = win.getch()

        if key == curses.KEY_UP:
            index = max(0, index - 1)
        elif key == curses.KEY_DOWN:
            index = min(len(matches) - 1, index + 1)
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            query = query[:-1]
            index = 0
        elif 32 <= key <= 126:
            query += chr(key)
            index = 0
        elif key in (10, 13):
            return matches[index] if matches else None
        elif key == 27:
            return None
