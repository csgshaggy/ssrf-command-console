# scripts/checks/__init__.py

import importlib
import os
import pkgutil

PACKAGE_DIR = os.path.dirname(__file__)
PACKAGE_NAME = __name__


def load_checks():
    checks = []

    # Iterate through all modules in this directory
    for _, mod_name, is_pkg in pkgutil.iter_modules([PACKAGE_DIR]):
        if is_pkg:
            continue

        # Skip utility modules — they are not checks
        if mod_name in {
            "baseline_snapshot",
            "diff_viewer",
            "regression_detector",
        }:
            continue

        module = importlib.import_module(f"{PACKAGE_NAME}.{mod_name}")

        # Only load modules that expose a run() function
        if hasattr(module, "run"):
            checks.append(module)

    # Deterministic ordering
    checks.sort(key=lambda m: m.__name__)
    return checks
