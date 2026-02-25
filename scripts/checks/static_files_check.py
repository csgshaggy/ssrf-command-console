# scripts/checks/static_files_check.py

import os
import requests


def run():
    base = os.environ.get("FASTAPI_BASE_URL", "http://127.0.0.1:8000")
    url = f"{base}/"
    static_url = f"{base}/static/"

    ok_root = False
    ok_static = False
    errors = []

    try:
        r = requests.get(url, timeout=3)
        ok_root = r.status_code == 200
        if not ok_root:
            errors.append(f"Root {url} -> {r.status_code}")
    except Exception as e:
        errors.append(f"Root {url} failed: {e}")

    try:
        r = requests.get(static_url, timeout=3)
        ok_static = r.status_code in (200, 301, 302, 403)
        if not ok_static:
            errors.append(f"Static {static_url} -> {r.status_code}")
    except Exception as e:
        errors.append(f"Static {static_url} failed: {e}")

    status = ok_root and ok_static
    details = "OK" if status else "; ".join(errors) if errors else "Unknown static issue"

    return {
        "name": "static_files_check",
        "status": status,
        "details": details,
        "data": {"base": base, "ok_root": ok_root, "ok_static": ok_static},
    }
