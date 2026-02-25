import curses
from app.core.tui_config import save_config


class FavoritesStore:
    """
    Stores user-selected favorite modes, persisted in config["favorites"].
    """

    def __init__(self, config):
        self.config = config
        self.favorites = list(config.get("favorites", []))

    def _sync(self):
        self.config["favorites"] = list(self.favorites)
        save_config(self.config)

    def add(self, mode: str):
        if mode not in self.favorites:
            self.favorites.append(mode)
            self._sync()

    def remove(self, mode: str):
        if mode in self.favorites:
            self.favorites.remove(mode)
            self._sync()

    def list(self):
        return self.favorites


def draw_favorites(screen, favorites: FavoritesStore):
    """
    Popup window showing scrollable favorites.
    Selecting a favorite returns the mode name.
    """
    favs = favorites.list()
    if not favs:
        favs = ["No favorites yet"]

    h, w = screen.getmaxyx()
    win_h = min(15, h - 4)
    win_w = min(40, w - 4)

    start_y = (h - win_h) // 2
    start_x = (w - win_w) // 2

    win = curses.newwin(win_h, win_w, start_y, start_x)
    win.keypad(True)
    win.border()

    index = 0

    while True:
        win.clear()
        win.border()
        win.addstr(0, 2, " Favorites ")

        visible = win_h - 4
        start = max(0, index - visible + 1)
        end = start + visible

        for i, mode in enumerate(favs[start:end]):
            if start + i == index:
                win.attron(curses.A_REVERSE)
                win.addstr(i + 2, 2, mode[: win_w - 4])
                win.attroff(curses.A_REVERSE)
            else:
                win.addstr(i + 2, 2, mode[: win_w - 4])

        win.refresh()

        key = win.getch()

        if key == curses.KEY_UP:
            index = max(0, index - 1)
        elif key == curses.KEY_DOWN:
            index = min(len(favs) - 1, index + 1)
        elif key in (10, 13):  # ENTER
            return favs[index] if favs[index] != "No favorites yet" else None
        elif key in (27, ord('q'), ord('F')):
            return None
