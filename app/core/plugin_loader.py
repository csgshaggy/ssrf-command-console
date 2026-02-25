import importlib.util
import os
from typing import Dict, Any, Callable


class Plugin:
    def __init__(self, name: str, module, modes: Dict[str, Any], runner: Callable):
        self.name = name
        self.module = module
        self.modes = modes
        self.runner = runner


def load_plugins(plugins_dir: str = "plugins") -> Dict[str, Plugin]:
    plugins: Dict[str, Plugin] = {}

    if not os.path.isdir(plugins_dir):
        return plugins

    for filename in os.listdir(plugins_dir):
        if not filename.endswith(".py"):
            continue

        path = os.path.join(plugins_dir, filename)
        name = os.path.splitext(filename)[0]

        spec = importlib.util.spec_from_file_location(name, path)
        if not spec or not spec.loader:
            continue

        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception:
            continue

        get_modes = getattr(module, "get_modes", None)
        run = getattr(module, "run", None)

        if not callable(get_modes) or not callable(run):
            continue

        try:
            modes = get_modes()
        except Exception:
            continue

        plugin = Plugin(name=name, module=module, modes=modes, runner=run)

        for mode_name in modes.keys():
            plugins[mode_name] = plugin

    return plugins
