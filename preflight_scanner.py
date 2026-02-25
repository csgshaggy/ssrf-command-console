#!/usr/bin/env python3
import os
import sys
import socket
import importlib

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
TARGETS_FILE = os.path.join(PROJECT_ROOT, "targets.txt")

def check_module(name):
    try:
        importlib.import_module(name)
        print(f"[OK] Python module: {name}")
        return True
    except ImportError as e:
        print(f"[ERROR] Missing module {name}: {e}")
        return False

def check_targets():
    if not os.path.exists(TARGETS_FILE):
        print(f"[ERROR] Missing targets file: {TARGETS_FILE}")
        return False
    with open(TARGETS_FILE) as f:
        lines = [l.strip() for l in f if l.strip()]
    if not lines:
        print(f"[ERROR] targets.txt is empty")
        return False
    print(f"[OK] targets.txt has {len(lines)} entries")
    return True

def check_port_free(port, host="0.0.0.0"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        if s.connect_ex((host, port)) == 0:
            print(f"[WARN] Port {port} appears in use")
            return False
        print(f"[OK] Port {port} appears free")
        return True

def main():
    os.chdir(PROJECT_ROOT)
    ok = True

    ok &= check_module("ssrf_scanner.parallel_scan")
    ok &= check_module("ssrf_scanner.dashboard_formatter")
    ok &= check_targets()
    ok &= check_port_free(5001)

    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
