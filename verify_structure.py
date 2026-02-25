#!/usr/bin/env python3
import os
import sys
import json

# ------------------------------------------------------------
# Colors
# ------------------------------------------------------------
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
BLUE = "\033[1;34m"
NC = "\033[0m"

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
STRICT_MODE = False       # If True: fail on missing directories
JSON_OUTPUT = False       # If True: output JSON instead of text

# Allowed top-level structure
ALLOWED_TOP_LEVEL = {
    "app",
    "console",
    "modes",
    "templates",
    "ssrf_scanner",
    "scripts",
    "dispatcher.py",
    "dashboard_web.py",
    "verify_structure.py",
    "requirements.txt",
    "favorites.json",
    ".gitignore",
    ".env",
}

# Directories that must exist
REQUIRED_DIRS = [
    "app",
    "console",
    "modes",
    "ssrf_scanner",
    "templates",
    "scripts",
]

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def print_header():
    if JSON_OUTPUT:
        return
    print(f"{BLUE}============================================================{NC}")
    print(f"{BLUE}        SSRF Command Console — Structure Verification       {NC}")
    print(f"{BLUE}============================================================{NC}")

def scan_top_level():
    return sorted(os.listdir("."))

def ensure_directories():
    created = []
    for d in REQUIRED_DIRS:
        if not os.path.exists(d):
            os.makedirs(d)
            created.append(d)
    return created

def recursive_scan(path):
    structure = {}
    for root, dirs, files in os.walk(path):
        structure[root] = {"dirs": dirs, "files": files}
    return structure

# ------------------------------------------------------------
# Main validation logic
# ------------------------------------------------------------
def validate():
    print_header()

    top = scan_top_level()

    missing = [d for d in REQUIRED_DIRS if not os.path.exists(d)]
    unexpected = [f for f in top if f not in ALLOWED_TOP_LEVEL]

    created = []
    if missing:
        print(f"{YELLOW}Missing required directories detected.{NC}")
        created = ensure_directories()
        if created:
            print(f"{GREEN}Auto-created:{NC}")
            for c in created:
                print(f"  - {c}")

    if JSON_OUTPUT:
        return {
            "missing": missing,
            "created": created,
            "unexpected": unexpected,
            "structure": recursive_scan("."),
        }

    # Human-readable output
    print()
    print(f"{BLUE}--- Missing Items ---{NC}")
    if missing:
        for m in missing:
            print(f"{RED}✘ Missing: {m}{NC}")
    else:
        print(f"{GREEN}✔ No missing required directories{NC}")

    print()
    print(f"{BLUE}--- Unexpected Items ---{NC}")
    if unexpected:
        print(f"{YELLOW}Unexpected files or directories:{NC}")
        for u in unexpected:
            print(f"  - {u}")
    else:
        print(f"{GREEN}✔ No unexpected items{NC}")

    print()
    print(f"{BLUE}--- Summary ---{NC}")
    print(f"{GREEN}✔ Required directories: {len(REQUIRED_DIRS)}{NC}")
    print(f"{GREEN}✔ Allowed top-level items: {len(ALLOWED_TOP_LEVEL)}{NC}")
    print(f"{GREEN}✔ Total items scanned: {len(top)}{NC}")

    print()
    print(f"{BLUE}============================================================{NC}")

    if STRICT_MODE and (missing or unexpected):
        print(f"{RED}STRICT MODE: Structure validation failed.{NC}")
        sys.exit(1)

    if unexpected:
        print(f"{YELLOW}NOTE:{NC} Unexpected items found. Review manually.")
        sys.exit(1)

    print(f"{GREEN}Structure OK — no anomalies detected.{NC}")
    sys.exit(0)

# ------------------------------------------------------------
# Entry point
# ------------------------------------------------------------
if __name__ == "__main__":
    result = validate()
    if JSON_OUTPUT:
        print(json.dumps(result, indent=2))
