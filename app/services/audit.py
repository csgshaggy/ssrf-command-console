import json
import time
from pathlib import Path

AUDIT_LOG = Path("logs/audit.log")


def write_audit_log(event: str, details: dict):
    """
    Append a structured JSON audit entry to logs/audit.log.
    Used by ops.py, auth.py, and any privileged action.
    """
    entry = {
        "timestamp": int(time.time()),
        "event": event,
        "details": details,
    }

    # Ensure logs directory exists
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)

    with AUDIT_LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")
