import sys
import os
import traceback

# Ensure project root is on PYTHONPATH
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.core.tui_app import TUIApp


def main():
    try:
        app = TUIApp()
        app.run()
    except Exception:
        print("TUI crashed:")
        print("".join(traceback.format_exc()))


if __name__ == "__main__":
    main()
