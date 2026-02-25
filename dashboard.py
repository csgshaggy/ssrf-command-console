#!/usr/bin/env python3
import curses
import requests
import json

BACKEND_URL = "http://127.0.0.1:5001"

MENU_ITEMS = [
    "Health",
    "Scan IPs",
    "Control: Ports",
    "Control: Processes",
    "Control: Manual Scan",
    "Control: Logs",
    "Quit",
]


def draw_menu(stdscr, current):
    stdscr.clear()
    stdscr.addstr(0, 0, "SSRF Console TUI Dashboard (↑/↓, Enter, q=quit)")
    for i, item in enumerate(MENU_ITEMS):
        marker = ">" if i == current else " "
        stdscr.addstr(2 + i, 0, f"{marker} {item}")
    stdscr.refresh()


def show_text(stdscr, title, text):
    stdscr.clear()
    stdscr.addstr(0, 0, title)
    lines = text.splitlines()
    h, w = stdscr.getmaxyx()
    for i, line in enumerate(lines[: h - 2]):
        stdscr.addstr(2 + i, 0, line[: w - 1])
    stdscr.addstr(h - 1, 0, "Press any key to return")
    stdscr.refresh()
    stdscr.getch()


def tui_main(stdscr):
    curses.curs_set(0)
    current = 0

    while True:
        draw_menu(stdscr, current)
        ch = stdscr.getch()

        if ch == ord("q"):
            break
        elif ch == curses.KEY_UP:
            current = (current - 1) % len(MENU_ITEMS)
        elif ch == curses.KEY_DOWN:
            current = (current + 1) % len(MENU_ITEMS)
        elif ch in (curses.KEY_ENTER, 10, 13):
            item = MENU_ITEMS[current]

            try:
                if item == "Health":
                    r = requests.get(f"{BACKEND_URL}/health", timeout=5)
                    show_text(stdscr, "Health", json.dumps(r.json(), indent=2))

                elif item == "Scan IPs":
                    curses.echo()
                    stdscr.clear()
                    stdscr.addstr(0, 0, "Enter comma-separated IPs: ")
                    ips = stdscr.getstr(1, 0).decode().strip()
                    curses.noecho()
                    ip_list = [x.strip() for x in ips.split(",") if x.strip()]
                    r = requests.post(
                        f"{BACKEND_URL}/scan",
                        json={"ips": ip_list, "workers": 10},
                        timeout=60,
                    )
                    show_text(stdscr, "Scan Results", json.dumps(r.json(), indent=2))

                elif item == "Control: Ports":
                    r = requests.get(f"{BACKEND_URL}/control/ports", timeout=5)
                    show_text(stdscr, "Ports", json.dumps(r.json(), indent=2))

                elif item == "Control: Processes":
                    r = requests.get(f"{BACKEND_URL}/control/processes", timeout=5)
                    show_text(stdscr, "Processes", json.dumps(r.json(), indent=2))

                elif item == "Control: Manual Scan":
                    r = requests.post(f"{BACKEND_URL}/control/manual_scan", timeout=30)
                    show_text(stdscr, "Manual Scan", json.dumps(r.json(), indent=2))

                elif item == "Control: Logs":
                    r = requests.get(f"{BACKEND_URL}/control/logs", timeout=10)
                    show_text(stdscr, "Logs", r.json().get("logs", ""))

                elif item == "Quit":
                    break

            except Exception as e:
                show_text(stdscr, "Error", f"{e}")


if __name__ == "__main__":
    curses.wrapper(tui_main)
