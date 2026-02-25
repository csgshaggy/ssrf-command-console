"""
ui.py
Rendering utilities for the SSRF Command Console TUI.

Handles:
- Clearing the screen
- Drawing banners and panels
- Consistent formatting
- Colorized output
- Paginated output
- Structured result viewer
"""

import os
from .colors import Colors, colorize


# -------------------------------------------------------------
# BASIC UI UTILITIES
# -------------------------------------------------------------
def clear():
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def banner(title="SSRF COMMAND CONSOLE"):
    """Render a top banner with a centered title."""
    width = 60
    line = "─" * width
    centered = title.center(width)

    print(colorize(f"┌{line}┐", Colors.CYAN))
    print(colorize(f"│{centered}│", Colors.CYAN + Colors.BOLD))
    print(colorize(f"└{line}┘", Colors.CYAN))


def panel(title, content_lines):
    """
    Draw a boxed panel with a title and multiple content lines.
    content_lines: list of strings
    """
    width = 60
    line = "─" * width
    title_line = f" {title} ".center(width)

    print(colorize(f"┌{line}┐", Colors.MAGENTA))
    print(colorize(f"│{title_line}│", Colors.MAGENTA + Colors.BOLD))
    print(colorize(f"├{line}┤", Colors.MAGENTA))

    for line in content_lines:
        padded = line.ljust(width)
        print(colorize(f"│{padded}│", Colors.MAGENTA))

    print(colorize(f"└{line}┘", Colors.MAGENTA))


def prompt(text):
    """Colorized input prompt."""
    return input(colorize(text, Colors.BRIGHT_GREEN + Colors.BOLD))


def section_header(text):
    """Print a bold section header."""
    print(colorize(f"\n{text}", Colors.BRIGHT_BLUE + Colors.BOLD))


def divider():
    """Print a simple divider line."""
    print(colorize("─" * 60, Colors.WHITE))


# -------------------------------------------------------------
# PAGINATION
# -------------------------------------------------------------
def paginate(lines, page_size=25):
    """Display long output in pages."""
    total = len(lines)
    index = 0

    while index < total:
        chunk = lines[index:index + page_size]
        for line in chunk:
            print(line)

        index += page_size

        if index < total:
            input(colorize("\n-- More -- Press Enter to continue --", Colors.YELLOW))


# -------------------------------------------------------------
# RESULT VIEWER
# -------------------------------------------------------------
def render_result_panel(result, analysis):
    """Pretty, colorized result + analysis viewer."""
    divider()
    section_header("RESULT")

    for key, value in result.items():
        if key == "mode":
            print(colorize(f"{key}: {value}", Colors.BRIGHT_CYAN + Colors.BOLD))
        else:
            print(colorize(f"{key}: {value}", Colors.GREEN))

    divider()
    section_header("ANALYSIS")

    for key, value in analysis.items():
        if isinstance(value, bool):
            color = Colors.BRIGHT_GREEN if value else Colors.BRIGHT_RED
            print(colorize(f"{key}: {value}", color))
        else:
            print(colorize(f"{key}: {value}", Colors.MAGENTA))

    divider()
