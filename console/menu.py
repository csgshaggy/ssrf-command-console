"""
menu.py
Main menu and navigation logic for the SSRF Command Console TUI.
"""

from .ui import (
    clear,
    banner,
    panel,
    prompt,
    section_header,
    divider,
    render_result_panel,
    paginate,
)
from .colors import Colors, colorize
from .history import HistoryManager
from .favorites import Favorites

from dispatcher import Dispatcher
from analyzer import Analyzer

import json
import subprocess


class ConsoleMenu:

    def __init__(self):
        self.dispatcher = Dispatcher()
        self.analyzer = Analyzer()
        self.history = HistoryManager()     # persistent history
        self.favorites = Favorites()        # persistent favorites

    # -------------------------------------------------------------
    # MAIN LOOP
    # -------------------------------------------------------------
    def start(self):
        while True:
            clear()
            banner("SSRF COMMAND CONSOLE")

            print(colorize("1. Run a Mode", Colors.GREEN))
            print(colorize("2. View Results History", Colors.CYAN))
            print(colorize("3. Generate New Mode", Colors.MAGENTA))
            print(colorize("4. Structure Check", Colors.YELLOW))
            print(colorize("5. Run Last Mode Again", Colors.BRIGHT_GREEN))
            print(colorize("6. Favorites", Colors.BRIGHT_MAGENTA))
            print(colorize("7. Diagnostics", Colors.BRIGHT_BLUE))
            print(colorize("8. Exit", Colors.RED))

            choice = prompt("\nSelect an option: ")

            if choice == "1":
                self.run_mode_menu()
            elif choice == "2":
                self.show_history()
            elif choice == "3":
                self.generate_mode()
            elif choice == "4":
                self.structure_check()
            elif choice == "5":
                self.run_last_mode()
            elif choice == "6":
                self.favorites_menu()
            elif choice == "7":
                self.diagnostics()
            elif choice == "8":
                clear()
                print(colorize("Goodbye.", Colors.BRIGHT_RED))
                return
            else:
                print(colorize("Invalid choice.", Colors.RED))
                input("Press Enter to continue...")

    # -------------------------------------------------------------
    # MODE RUNNER
    # -------------------------------------------------------------
    def run_mode_menu(self):
        clear()
        banner("RUN A MODE")

        modes = self.dispatcher.list_modes()
        panel("Available Modes", [f"{i+1}. {m}" for i, m in enumerate(modes)])

        choice = prompt("\nSelect a mode number: ")

        try:
            idx = int(choice) - 1
            mode_name = modes[idx]
        except:
            print(colorize("Invalid selection.", Colors.RED))
            input("Press Enter to continue...")
            return

        target = prompt("Enter target (or leave blank): ")
        options_raw = prompt("Enter options as JSON (or leave blank): ")

        try:
            options = json.loads(options_raw) if options_raw else {}
        except:
            print(colorize("Invalid JSON.", Colors.RED))
            input("Press Enter to continue...")
            return

        clear()
        banner(f"RUNNING MODE: {mode_name}")

        result = self.dispatcher.run_mode(mode_name, target, options)
        analysis = self.analyzer.analyze(result)

        # Save to persistent history
        self.history.add(mode_name, result, analysis)

        render_result_panel(result, analysis)
        input("\nPress Enter to return to menu...")

    # -------------------------------------------------------------
    # RUN LAST MODE AGAIN
    # -------------------------------------------------------------
    def run_last_mode(self):
        entries = self.history.all()
        if not entries:
            print(colorize("No previous mode to run.", Colors.YELLOW))
            input("Press Enter to continue...")
            return

        last = entries[-1]
        mode = last["mode"]
        target = last["result"].get("target", "")
        options = last["result"].get("options", {})

        clear()
        banner(f"RE-RUNNING LAST MODE: {mode}")

        result = self.dispatcher.run_mode(mode, target, options)
        analysis = self.analyzer.analyze(result)

        self.history.add(mode, result, analysis)
        render_result_panel(result, analysis)

        input("\nPress Enter to return to menu...")

    # -------------------------------------------------------------
    # HISTORY VIEWER
    # -------------------------------------------------------------
    def show_history(self):
        clear()
        banner("RESULTS HISTORY")

        entries = self.history.all()

        if not entries:
            print(colorize("No history yet.", Colors.YELLOW))
            input("Press Enter to continue...")
            return

        for i, entry in enumerate(entries):
            divider()
            print(colorize(f"[{i+1}] Mode: {entry['mode']}", Colors.CYAN))
            print(colorize(f"Timestamp: {entry['timestamp']}", Colors.BRIGHT_BLUE))
            render_result_panel(entry["result"], entry["analysis"])

        divider()
        input("\nPress Enter to return to menu...")

    # -------------------------------------------------------------
    # FAVORITES SYSTEM
    # -------------------------------------------------------------
    def favorites_menu(self):
        clear()
        banner("FAVORITES")

        favs = self.favorites.all()

        if not favs:
            print(colorize("No favorites yet.", Colors.YELLOW))
        else:
            panel("Favorite Modes", [f"{i+1}. {m}" for i, m in enumerate(favs)])

        print(colorize("\n1. Add Favorite", Colors.GREEN))
        print(colorize("2. Remove Favorite", Colors.RED))
        print(colorize("3. Back", Colors.CYAN))

        choice = prompt("\nSelect: ")

        if choice == "1":
            mode = prompt("Enter mode name to add: ")
            self.favorites.add(mode)
        elif choice == "2":
            mode = prompt("Enter mode name to remove: ")
            self.favorites.remove(mode)

        input("Press Enter to continue...")

    # -------------------------------------------------------------
    # MODE GENERATOR
    # -------------------------------------------------------------
    def generate_mode(self):
        clear()
        banner("MODE GENERATOR")

        name = prompt("Enter new mode name: ")

        try:
            subprocess.run(["python3", "mode_template.py", name])
            print(colorize(f"Mode '{name}' generated.", Colors.GREEN))
        except Exception as e:
            print(colorize(f"Error generating mode: {e}", Colors.RED))

        input("Press Enter to continue...")

    # -------------------------------------------------------------
    # STRUCTURE CHECK
    # -------------------------------------------------------------
    def structure_check(self):
        clear()
        banner("STRUCTURE CHECK")

        try:
            output = subprocess.check_output(["python3", "verify_structure.py"])
            lines = output.decode().splitlines()
            paginate(lines)
        except Exception as e:
            print(colorize(f"Error running structure check: {e}", Colors.RED))

        input("Press Enter to continue...")

    # -------------------------------------------------------------
    # DIAGNOSTICS PANEL
    # -------------------------------------------------------------
    def diagnostics(self):
        clear()
        banner("SYSTEM DIAGNOSTICS")

        import platform
        import shutil

        lines = [
            f"Python Version: {platform.python_version()}",
            f"Platform: {platform.system()} {platform.release()}",
            f"Dispatcher Modes: {len(self.dispatcher.list_modes())}",
            f"History Entries: {len(self.history.all())}",
            f"Favorites: {len(self.favorites.all())}",
            f"Git Present: {'Yes' if shutil.which('git') else 'No'}",
        ]

        panel("Diagnostics Summary", lines)
        input("Press Enter to continue...")
