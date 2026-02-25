import sys
import os
import curses

ROOT = os.path.abspath(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from dispatcher import Dispatcher
from app.core.tui_app import TUIApp


def main():
    dispatcher = Dispatcher()
    app = TUIApp(dispatcher)

    dispatcher.state = app.state
    app.state.available_modes = list(dispatcher.modes.keys())

    curses.wrapper(app.run)


if __name__ == "__main__":
    main()
