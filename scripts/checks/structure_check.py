# scripts/checks/structure_check.py

import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def run():
    expected_dirs = [
        "app",
        "scripts",
        "scripts/checks",
    ]

    missing = []
    for d in expected_dirs:
        if not os.path.isdir(os.path.join(ROOT_DIR, d)):
            missing.append(d)

    status = not missing
    details = "OK" if status else f"Missing dirs: {', '.join(missing)}"

    # Snapshot directory structure
    structure = []
    for base, dirs, files in os.walk(ROOT_DIR):
        rel = os.path.relpath(base, ROOT_DIR)

        # Skip noise
        if rel.startswith(".git") or rel.startswith("__pycache__") or rel.startswith("venv"):
            continue

        structure.append(
            {
                "dir": rel,
                "dirs": sorted(dirs),
                "files": sorted(files),
            }
        )

    return {
        "name": "structure_check",
        "status": status,
        "details": details,
        "data": {"structure": structure},
    }
