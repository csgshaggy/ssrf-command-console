import curses
from app.core.tui_config import save_config

# Base option schema; values will be overridden from config["mode_options"] if present.
BASE_MODE_OPTIONS = {
    "header_probe_mode": {
        "follow_redirects": {"type": "bool", "value": True},
        "timeout": {"type": "int", "value": 5},
    },
    "metadata_mode": {
        "include_headers": {"type": "bool", "value": True},
        "include_body": {"type": "bool", "value": False},
    },
    "dns_mode": {
        "record_type": {"type": "choice", "choices": ["A", "AAAA", "CNAME", "MX"], "value": "A"},
        "recursive": {"type": "bool", "value": True},
    },
}


def _build_schema_for_mode(mode_name: str, config):
    """
    Merge base schema with persisted values from config["mode_options"].
    """
    base = BASE_MODE_OPTIONS.get(mode_name)
    if not base:
        return None

    persisted = config.get("mode_options", {}).get(mode_name, {})
    schema = {}

    for key, opt in base.items():
        schema[key] = opt.copy()
        if key in persisted:
            schema[key]["value"] = persisted[key]

    return schema


def _persist_schema(mode_name: str, schema, config):
    """
    Write current option values back into config["mode_options"] and save.
    """
    if "mode_options" not in config or not isinstance(config["mode_options"], dict):
        config["mode_options"] = {}

    config["mode_options"][mode_name] = {k: schema[k]["value"] for k in schema.keys()}
    save_config(config)


def draw_mode_options(screen, mode_name: str, config):
    """
    Popup window for editing mode-specific options.
    Returns a dict of option values.
    Persists changes into config.
    """
    schema = _build_schema_for_mode(mode_name, config)
    if not schema:
        return {}  # No options for this mode

    h, w = screen.getmaxyx()
    win_h = min(20, h - 4)
    win_w = min(60, w - 4)

    start_y = (h - win_h) // 2
    start_x = (w - win_w) // 2

    win = curses.newwin(win_h, win_w, start_y, start_x)
    win.keypad(True)

    keys = list(schema.keys())
    index = 0

    while True:
        win.clear()
        win.border()
        win.addstr(0, 2, f" Options: {mode_name} ")

        for i, key in enumerate(keys):
            opt = schema[key]
            val = opt["value"]

            if opt["type"] == "bool":
                display = f"{key}: {'ON' if val else 'OFF'}"
            elif opt["type"] == "int":
                display = f"{key}: {val}"
            elif opt["type"] == "choice":
                display = f"{key}: {val} (choices: {', '.join(opt['choices'])})"
            else:
                display = f"{key}: {val}"

            if i == index:
                win.attron(curses.A_REVERSE)
                win.addstr(i + 2, 2, display[: win_w - 4])
                win.attroff(curses.A_REVERSE)
            else:
                win.addstr(i + 2, 2, display[: win_w - 4])

        win.refresh()
        keypress = win.getch()

        if keypress == curses.KEY_UP:
            index = max(0, index - 1)
        elif keypress == curses.KEY_DOWN:
            index = min(len(keys) - 1, index + 1)
        elif keypress in (10, 13, 27):  # ENTER or ESC = accept
            _persist_schema(mode_name, schema, config)
            return {k: schema[k]["value"] for k in keys}

        # Modify selected option
        opt = schema[keys[index]]

        if opt["type"] == "bool":
            if keypress in (curses.KEY_LEFT, curses.KEY_RIGHT, ord(' ')):
                opt["value"] = not opt["value"]

        elif opt["type"] == "int":
            if keypress == curses.KEY_LEFT:
                opt["value"] = max(0, opt["value"] - 1)
            elif keypress == curses.KEY_RIGHT:
                opt["value"] += 1

        elif opt["type"] == "choice":
            choices = opt["choices"]
            cur = choices.index(opt["value"])
            if keypress == curses.KEY_LEFT:
                opt["value"] = choices[(cur - 1) % len(choices)]
            elif keypress == curses.KEY_RIGHT:
                opt["value"] = choices[(cur + 1) % len(choices)]
