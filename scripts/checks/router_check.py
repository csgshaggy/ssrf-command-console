# scripts/checks/router_check.py

import importlib

APP_MODULE = "app.main"  # Adjust if your FastAPI entrypoint differs


def run():
    try:
        mod = importlib.import_module(APP_MODULE)
        app = getattr(mod, "app", None)
    except Exception as e:
        return {
            "name": "router_check",
            "status": False,
            "details": f"Failed to import app: {e}",
            "data": {"routes": []},
        }

    if app is None:
        return {
            "name": "router_check",
            "status": False,
            "details": "No 'app' object found in app.main",
            "data": {"routes": []},
        }

    routes = []
    for r in app.routes:
        path = getattr(r, "path", None)
        methods = getattr(r, "methods", None)
        if path:
            routes.append({"path": path, "methods": sorted(methods) if methods else []})

    return {
        "name": "router_check",
        "status": True,
        "details": f"{len(routes)} routes",
        "data": {"routes": routes},
    }
