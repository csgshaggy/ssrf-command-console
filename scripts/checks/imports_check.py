# scripts/checks/imports_check.py

import os
import pkgutil
import importlib

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
APP_PACKAGE = "app"


def run():
    os.chdir(ROOT_DIR)
    broken = []

    try:
        pkg = importlib.import_module(APP_PACKAGE)
    except Exception as e:
        return {
            "name": "imports_check",
            "status": False,
            "details": f"Failed to import app: {e}",
            "data": {"broken": ["app"]},
        }

    pkg_path = pkg.__path__

    for _, mod_name, is_pkg in pkgutil.walk_packages(pkg_path, prefix=f"{APP_PACKAGE}."):
        try:
            importlib.import_module(mod_name)
        except Exception as e:
            broken.append(f"{mod_name}: {e}")

    status = not broken
    details = "OK" if status else f"{len(broken)} broken imports"

    return {
        "name": "imports_check",
        "status": status,
        "details": details,
        "data": {"broken": broken},
    }
