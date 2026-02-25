import json
import os
from typing import Dict, Any

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".ssrf_console_tui.json")

DEFAULT_CONFIG: Dict[str, Any] = {
    "favorites": [],
    "mode_options": {},  # mode_name -> {option_name: value}
}


def load_config() -> Dict[str, Any]:
    if not os.path.exists(CONFIG_PATH):
        return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)
        # Merge with defaults to avoid missing keys
        cfg = DEFAULT_CONFIG.copy()
        cfg.update(data)
        if "favorites" not in cfg or not isinstance(cfg["favorites"], list):
            cfg["favorites"] = []
        if "mode_options" not in cfg or not isinstance(cfg["mode_options"], dict):
            cfg["mode_options"] = {}
        return cfg
    except Exception:
        return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any]) -> None:
    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)
    except Exception:
        # Silent failure: TUI should never crash on save
        pass
