# scripts/checks/fastapi_health_check.py

import os
import requests


def run():
    url = os.environ.get("FASTAPI_HEALTH_URL", "http://127.0.0.1:8000/health")

    try:
        resp = requests.get(url, timeout=3)
        status = resp.status_code == 200
        details = f"{resp.status_code} from {url}"
    except Exception as e:
        status = False
        details = f"Health check failed: {e}"

    return {
        "name": "fastapi_health_check",
        "status": status,
        "details": details,
        "data": {"url": url, "status": status},
    }
