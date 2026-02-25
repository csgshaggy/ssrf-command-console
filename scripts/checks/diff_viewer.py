# scripts/checks/diff_viewer.py

from copy import deepcopy

try:
    from colorama import Fore, Style
except ImportError:
    class F:
        RED = GREEN = YELLOW = CYAN = ""
    class S:
        RESET_ALL = ""
    Fore, Style = F(), S()


def compute_diffs(baseline, current):
    diffs = {
        "checks_added": [],
        "checks_removed": [],
        "checks_status_changed": [],
        "data_changed": [],
    }

    base_keys = set(baseline.keys())
    curr_keys = set(current.keys())

    diffs["checks_added"] = sorted(curr_keys - base_keys)
    diffs["checks_removed"] = sorted(base_keys - curr_keys)

    for name in base_keys & curr_keys:
        b = baseline[name]
        c = current[name]

        if b.get("status") != c.get("status"):
            diffs["checks_status_changed"].append(
                {
                    "name": name,
                    "baseline": b.get("status"),
                    "current": c.get("status"),
                }
            )

        if deepcopy(b.get("data")) != deepcopy(c.get("data")):
            diffs["data_changed"].append(name)

    return diffs


def print_diffs(diffs):
    print(f"{Fore.CYAN}=== Baseline Drift ==={Style.RESET_ALL}")

    if not any(diffs.values()):
        print(f"{Fore.GREEN}No drift detected.{Style.RESET_ALL}\n")
        return

    if diffs["checks_added"]:
        print(f"{Fore.YELLOW}Checks added:{Style.RESET_ALL}")
        for name in diffs["checks_added"]:
            print(f"  + {name}")

    if diffs["checks_removed"]:
        print(f"{Fore.YELLOW}Checks removed:{Style.RESET_ALL}")
        for name in diffs["checks_removed"]:
            print(f"  - {name}")

    if diffs["checks_status_changed"]:
        print(f"{Fore.YELLOW}Checks status changed:{Style.RESET_ALL}")
        for item in diffs["checks_status_changed"]:
            print(
                f"  * {item['name']}: "
                f"{item['baseline']} -> {item['current']}"
            )

    if diffs["data_changed"]:
        print(f"{Fore.YELLOW}Checks with data drift:{Style.RESET_ALL}")
        for name in diffs["data_changed"]:
            print(f"  * {name}")

    print()
