"""
colors.py
Centralized ANSI color definitions + theme system.
"""

class Colors:
    RESET = "\033[0m"

    # Base palette (default theme)
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# -------------------------------------------------------------
# THEMES
# -------------------------------------------------------------
THEMES = {
    "default": {
        "primary": Colors.CYAN,
        "accent": Colors.MAGENTA,
        "success": Colors.GREEN,
        "warning": Colors.YELLOW,
        "error": Colors.RED,
        "info": Colors.BRIGHT_BLUE,
    },
    "hacker": {
        "primary": Colors.GREEN,
        "accent": Colors.BRIGHT_GREEN,
        "success": Colors.BRIGHT_GREEN,
        "warning": Colors.YELLOW,
        "error": Colors.RED,
        "info": Colors.GREEN,
    },
    "blue_steel": {
        "primary": Colors.BRIGHT_BLUE,
        "accent": Colors.BLUE,
        "success": Colors.BRIGHT_CYAN,
        "warning": Colors.BRIGHT_YELLOW,
        "error": Colors.BRIGHT_RED,
        "info": Colors.BRIGHT_BLUE,
    },
    "grayscale": {
        "primary": Colors.WHITE,
        "accent": Colors.BRIGHT_WHITE,
        "success": Colors.WHITE,
        "warning": Colors.WHITE,
        "error": Colors.WHITE,
        "info": Colors.WHITE,
    },
    "high_contrast": {
        "primary": Colors.BRIGHT_WHITE,
        "accent": Colors.BRIGHT_YELLOW,
        "success": Colors.BRIGHT_GREEN,
        "warning": Colors.BRIGHT_YELLOW,
        "error": Colors.BRIGHT_RED,
        "info": Colors.BRIGHT_CYAN,
    },
}

current_theme = THEMES["default"]


def set_theme(name):
    global current_theme
    if name in THEMES:
        current_theme = THEMES[name]


def theme_color(key):
    return current_theme.get(key, Colors.WHITE)


def colorize(text, color):
    return f"{color}{text}{Colors.RESET}"
