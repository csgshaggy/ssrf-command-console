# Layout definitions for the TUI engine.
# Each layout is a dictionary of region sizes.

LAYOUTS = {
    "default": {
        "header": 1,     # top bar
        "footer": 1,     # bottom bar
        "sidebar": 22,   # left column width
        "status": 1,     # status line above footer
    },

    "compact": {
        "header": 1,
        "footer": 1,
        "sidebar": 18,
        "status": 1,
    },

    "wide": {
        "header": 1,
        "footer": 1,
        "sidebar": 30,
        "status": 1,
    },
}
