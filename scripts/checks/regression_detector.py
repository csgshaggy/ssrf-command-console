# scripts/checks/regression_detector.py

try:
    from colorama import Fore, Style
except ImportError:
    class F:
        RED = GREEN = YELLOW = CYAN = ""
    class S:
        RESET_ALL = ""
    Fore, Style = F(), S()


def detect_regressions(baseline, current, diffs):
    regressions = []

    # 1) Checks that passed before but now fail
    for name, base_entry in baseline.items():
        curr_entry = current.get(name)
        if not curr_entry:
            continue
        if base_entry.get("status") and not curr_entry.get("status"):
            regressions.append(
                {
                    "type": "check_status_regression",
                    "check": name,
                    "detail": "Previously passed, now failing.",
                }
            )

    # 2) Data drift in critical checks
    critical = {
        "structure_check",
        "imports_check",
        "router_check",
        "static_files_check",
    }

    for name in diffs.get("data_changed", []):
        if name in critical:
            regressions.append(
                {
                    "type": "data_drift_regression",
                    "check": name,
                    "detail": "Critical check data drift detected.",
                }
            )

    return regressions


def print_regressions(regressions):
    print(f"{Fore.CYAN}=== Regressions ==={Style.RESET_ALL}")

    if not regressions:
        print(f"{Fore.GREEN}None.{Style.RESET_ALL}\n")
        return

    for r in regressions:
        print(
            f"{Fore.RED}- [{r['type']}] {r['check']}: "
            f"{r['detail']}{Style.RESET_ALL}"
        )

    print()
