#!/usr/bin/env python
import argparse
import json
import os
import sys
from datetime import datetime

from checks import load_checks
from checks.baseline_snapshot import (
    save_baseline_snapshot,
    load_current_baseline,
    ensure_baseline_dirs,
)
from checks.diff_viewer import compute_diffs, print_diffs
from checks.regression_detector import detect_regressions, print_regressions

try:
    from colorama import Fore, Style, init as colorama_init
except ImportError:
    class Dummy:
        RESET_ALL = ""
    class F:
        RED = GREEN = YELLOW = CYAN = ""
    colorama_init = lambda: None
    Fore, Style = F(), Dummy()

colorama_init(autoreset=True)

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASELINE_DIR = os.path.join(ROOT_DIR, "baseline")
CURRENT_BASELINE_DIR = os.path.join(BASELINE_DIR, "current")
HISTORY_DIR = os.path.join(BASELINE_DIR, "history")


def color_status(ok: bool) -> str:
    return f"{Fore.GREEN}✓{Style.RESET_ALL}" if ok else f"{Fore.RED}✗{Style.RESET_ALL}"


def run_checks():
    checks = load_checks()
    results = []
    for check in checks:
        try:
            res = check.run()
            # normalize
            res.setdefault("status", False)
            res.setdefault("name", check.__name__)
            res.setdefault("details", "")
            res.setdefault("data", {})
        except Exception as e:
            res = {
                "name": getattr(check, "__name__", "unknown"),
                "status": False,
                "details": f"Exception: {e}",
                "data": {},
            }
        results.append(res)
    return results


def print_summary(results):
    print()
    print(f"{Fore.CYAN}=== Environment Check Summary ==={Style.RESET_ALL}")
    for r in results:
        print(f"[{color_status(r['status'])}] {r['name']:<24} — {r['details']}")
    print()


def aggregate_data(results):
    """Collect per-check data into a single dict for baseline/regression."""
    agg = {}
    for r in results:
        name = r["name"]
        agg[name] = {
            "status": r["status"],
            "data": r.get("data", {}),
        }
    return agg


def main():
    parser = argparse.ArgumentParser(description="Environment preflight + baseline + regression detector")
    parser.add_argument(
        "--snapshot",
        action="store_true",
        help="Create a new baseline snapshot (also stored in history).",
    )
    parser.add_argument(
        "--no-regression",
        action="store_true",
        help="Skip regression detection (just run checks).",
    )
    args = parser.parse_args()

    os.chdir(ROOT_DIR)
    ensure_baseline_dirs(BASELINE_DIR, CURRENT_BASELINE_DIR, HISTORY_DIR)

    print(f"{Fore.CYAN}Running environment checks from:{Style.RESET_ALL} {ROOT_DIR}")
    results = run_checks()
    print_summary(results)

    agg = aggregate_data(results)

    # Save snapshot if requested
    if args.snapshot:
        ts = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
        save_baseline_snapshot(
            agg,
            CURRENT_BASELINE_DIR,
            HISTORY_DIR,
            timestamp=ts,
        )
        print(f"{Fore.YELLOW}Baseline snapshot saved at timestamp:{Style.RESET_ALL} {ts}")

    # Load current baseline (if exists)
    baseline = load_current_baseline(CURRENT_BASELINE_DIR)

    # Diff + regression
    if baseline and not args.no_regression:
        diffs = compute_diffs(baseline, agg)
        print_diffs(diffs)

        regressions = detect_regressions(baseline, agg, diffs)
        print_regressions(regressions)
    elif not baseline:
        print(f"{Fore.YELLOW}No current baseline found. Run with --snapshot after a clean state.{Style.RESET_ALL}")

    # Exit code
    overall_ok = all(r["status"] for r in results)
    if not overall_ok:
        print(f"{Fore.RED}Environment Status: FAILED{Style.RESET_ALL}")
        sys.exit(1)

    print(f"{Fore.GREEN}Environment Status: CLEAN{Style.RESET_ALL}")
    sys.exit(0)


if __name__ == "__main__":
    main()
