import os
import datetime
from typing import Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
CRASH_DIR = os.path.join(LOG_DIR, "crash_reports")

os.makedirs(CRASH_DIR, exist_ok=True)


def write_crash_report(exc: Exception, traceback_str: str, context: Optional[str] = None) -> str:
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S-%f")
    filename = f"crash-{timestamp}.log"
    path = os.path.join(CRASH_DIR, filename)

    lines = [
        f"Timestamp (UTC): {timestamp}",
        f"Exception type: {type(exc).__name__}",
        f"Exception: {exc}",
    ]
    if context:
        lines.append(f"Context: {context}")
    lines.append("\nTraceback:")
    lines.append(traceback_str)

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[CRASH] Crash report written to: {path}")
    return path
