import curses


class TUIEngine:
    def __init__(self, stdscr, dispatcher, state):
        self.stdscr = stdscr
        self.dispatcher = dispatcher
        self.state = state

    def run(self):
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        self.stdscr.nodelay(False)
        self.stdscr.keypad(True)

        while True:
            self.draw()
            ch = self.stdscr.getch()
            if not self.handle_key(ch):
                break

    def draw(self):
        self.stdscr.erase()
        h, w = self.stdscr.getmaxyx()

        sidebar_width = max(20, int(w * 0.25))
        output_width = w - sidebar_width - 1

        sidebar = self.stdscr.derwin(h - 2, sidebar_width, 0, 0)
        output = self.stdscr.derwin(h - 2, output_width, 0, sidebar_width + 1)
        status = self.stdscr.derwin(2, w, h - 2, 0)

        self.draw_sidebar(sidebar)
        self.draw_output(output)
        self.draw_status(status)

        self.stdscr.refresh()

    def draw_sidebar(self, win):
        win.box()
        win.addstr(0, 2, " Modes ")

        for idx, name in enumerate(self.state.available_modes):
            y = idx + 1
            if y >= win.getmaxyx()[0] - 1:
                break
            if idx == self.state.selected_mode_index:
                win.attron(curses.A_REVERSE)
                win.addnstr(y, 1, name, win.getmaxyx()[1] - 2)
                win.attroff(curses.A_REVERSE)
            else:
                win.addnstr(y, 1, name, win.getmaxyx()[1] - 2)

    def draw_output(self, win):
        win.box()
        win.addstr(0, 2, " Output ")

        h, w = win.getmaxyx()
        max_lines = h - 2
        lines = self.state.output_lines
        start = self.state.output_scroll
        end = start + max_lines

        for idx, line in enumerate(lines[start:end]):
            color = curses.color_pair(0)
            if "ERROR" in line:
                color = curses.color_pair(2)
            elif "SUCCESS" in line or "OK" in line:
                color = curses.color_pair(1)
            elif "WARN" in line:
                color = curses.color_pair(3)

            win.addnstr(1 + idx, 1, line, w - 2, color)

    def draw_status(self, win):
        win.erase()
        h, w = win.getmaxyx()
        text = f"Target: {self.state.target} | Q: Quit | Enter: Run | T: Set Target | PgUp/PgDn: Scroll"
        win.addnstr(0, 1, text, w - 2)

    def handle_key(self, ch):
        if ch in (ord('q'), ord('Q')):
            return False

        if ch == curses.KEY_UP:
            if self.state.selected_mode_index > 0:
                self.state.selected_mode_index -= 1

        elif ch == curses.KEY_DOWN:
            if self.state.selected_mode_index < len(self.state.available_modes) - 1:
                self.state.selected_mode_index += 1

        elif ch == curses.KEY_NPAGE:  # Page Down
            if self.state.output_scroll + 1 < max(0, len(self.state.output_lines) - 1):
                self.state.output_scroll += 1

        elif ch == curses.KEY_PPAGE:  # Page Up
            if self.state.output_scroll > 0:
                self.state.output_scroll -= 1

        elif ch in (10, 13):  # Enter
            self.run_selected_mode()

        elif ch in (ord('t'), ord('T')):
            self.prompt_for_target()

        return True

    def run_selected_mode(self):
        if not self.state.available_modes:
            self.state.output_lines = ["[ERROR] No modes loaded"]
            return

        name = self.state.available_modes[self.state.selected_mode_index]
        lines = self.dispatcher.run_mode_with_context(
            name,
            target=self.state.target,
            options=self.state.options,
            state=self.state,
        )
        self.state.output_lines = lines
        self.state.output_scroll = 0

    def prompt_for_target(self):
        h, w = self.stdscr.getmaxyx()
        prompt = "Target URL: "

        curses.echo()
        self.stdscr.move(h - 2, 0)
        self.stdscr.clrtoeol()
        self.stdscr.addstr(h - 2, 1, prompt)
        self.stdscr.refresh()

        value = self.stdscr.getstr(h - 2, 1 + len(prompt), w - len(prompt) - 2)
        curses.noecho()

        try:
            self.state.target = value.decode("utf-8").strip()
        except Exception:
            self.state.target = ""
