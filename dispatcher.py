import os
import importlib


class Dispatcher:
    def __init__(self):
        self.modes = {}
        self.state = None
        self._load_modes()

    def register_mode(self, name, func):
        if name not in self.modes:
            self.modes[name] = func

    def _load_modes(self):
        root = os.path.dirname(os.path.abspath(__file__))
        modes_dir = os.path.join(root, "modes")

        if not os.path.isdir(modes_dir):
            return

        for filename in os.listdir(modes_dir):
            if not filename.endswith("_mode.py"):
                continue

            module_name = filename[:-3]
            import_path = f"modes.{module_name}"

            try:
                module = importlib.import_module(import_path)
                for attr in dir(module):
                    if attr.endswith("_mode"):
                        func = getattr(module, attr)
                        if callable(func):
                            self.register_mode(attr, func)
            except Exception:
                continue

    def run_mode(self, name):
        if name not in self.modes:
            return [f"[ERROR] Mode not found: {name}"]

        try:
            result = self.modes[name]()
            if isinstance(result, list):
                return [str(x) for x in result]
            return [str(result)]
        except Exception as e:
            return [f"[ERROR] Exception in mode '{name}': {e}"]

    def run_mode_with_context(self, name, target=None, options=None, state=None):
        if name not in self.modes:
            return [f"[ERROR] Mode not found: {name}"]

        func = self.modes[name]

        try:
            result = func(target=target, options=options, state=state, dispatcher=self)
        except TypeError:
            result = func()

        if isinstance(result, list):
            return [str(x) for x in result]
        elif result is None:
            return []
        else:
            return [str(result)]
