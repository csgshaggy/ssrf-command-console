#!/usr/bin/env python3
import os
import sys
import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

REQUIRED_DIRS = ["logs", "pids", "crash_reports", "ssrf_scanner", "ssrf_manager"]
REQUIRED_FILES = ["main.py", "dashboard_web.py", "dashboard.py", "config.yaml"]

def main():
    ok = True

    if not os.path.exists(CONFIG_PATH):
        print(f"[ERROR] Missing config.yaml at {CONFIG_PATH}")
        sys.exit(1)

    with open(CONFIG_PATH, "r") as f:
        cfg = yaml.safe_load(f)

    project_root = cfg.get("project_root")
    if not project_root or not os.path.isdir(project_root):
        print(f"[ERROR] Invalid or missing project_root: {project_root}")
        ok = False
    else:
        print(f"[OK] project_root: {project_root}")

    for d in REQUIRED_DIRS:
        path = os.path.join(project_root, d)
        if os.path.isdir(path):
            print(f"[OK] dir: {path}")
        else:
            print(f"[MISSING] dir: {path}")
            ok = False

    for fpath in REQUIRED_FILES:
        path = os.path.join(project_root, fpath)
        if os.path.isfile(path):
            print(f"[OK] file: {path}")
        else:
            print(f"[MISSING] file: {path}")
            ok = False

    comps = cfg.get("components", {})
    for name, meta in comps.items():
        if "path" in meta:
            path = os.path.join(project_root, meta["path"])
            if os.path.isfile(path):
                print(f"[OK] component {name}: {path}")
            else:
                print(f"[MISSING] component {name}: {path}")
                ok = False

    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
