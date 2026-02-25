import curses
from dataclasses import dataclass, field


@dataclass
class AppState:
    available_modes: list = field(default_factory=list)
    selected_mode_index: int = 0
    output_lines: list = field(default_factory=list)
    output_scroll: int = 0
    target: str = "http://127.0.0.1"
    options: dict = field(default_factory=dict)


class TUIApp:
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.state = AppState()
        self.engine = None

    def run(self, stdscr):
        from app.core.tui_engine import TUIEngine
        self.engine = TUIEngine(stdscr, self.dispatcher, self.state)
        self.engine.run()
