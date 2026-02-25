import time
import requests
from typing import Optional


def wait_for_http(
    url: str,
    timeout_seconds: int = 30,
    interval_seconds: float = 1.0,
    name: Optional[str] = None,
) -> None:
    label = name or url
    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
        try:
            resp = requests.get(url, timeout=3)
            if resp.status_code < 500:
                print(f"[HEALTH] {label} is up (status={resp.status_code})")
                return
        except Exception:
            pass

        print(f"[HEALTH] Waiting for {label} ...")
        time.sleep(interval_seconds)

    raise RuntimeError(f"Timeout waiting for dependency: {label}")


def wait_for_dependencies() -> None:
    print("[HEALTH] No external dependencies configured for bootstrap.")
