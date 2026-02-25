#!/usr/bin/env python3
import subprocess
import sys
import os
import time

PROJECT_ROOT = "/home/kali/SSRF_CONSOLE"
SCANNER_PATH = os.path.join(PROJECT_ROOT, "ssrf_scanner", "ssrf_scanner.py")

process = None

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


def start_scanner():
    global process

    if not os.path.exists(SCANNER_PATH):
        print(f"{RED}[ERROR]{RESET} Scanner not found at: {SCANNER_PATH}")
        return

    print(f"{GREEN}[+] Starting SSRF Scanner...{RESET}")
    try:
        process = subprocess.Popen(["python3", SCANNER_PATH])
        print(f"{GREEN}[OK]{RESET} Scanner running (PID {process.pid})")
    except Exception as e:
        print(f"{RED}[ERROR]{RESET} Failed to start scanner: {e}")


def stop_scanner():
    global process

    if not process:
        print(f"{YELLOW}[!] Scanner is not running{RESET}")
        return

    print(f"{YELLOW}[-] Stopping scanner...{RESET}")
    try:
        process.terminate()
        process.wait(timeout=5)
        print(f"{GREEN}[OK]{RESET} Scanner stopped")
        process = None
    except Exception:
        print(f"{RED}[!] Force killing scanner{RESET}")
        process.kill()
        process = None


def restart_scanner():
    stop_scanner()
    time.sleep(1)
    start_scanner()


def health_check():
    if process and process.poll() is None:
        print(f"{GREEN}[RUNNING]{RESET} SSRF Scanner (PID {process.pid})")
    else:
        print(f"{RED}[STOPPED]{RESET} SSRF Scanner")


def menu():
    while True:
        print(f"""
{CYAN}==========================================
           SSRF SCANNER LAUNCHER
=========================================={RESET}
1. Start Scanner
2. Stop Scanner
3. Restart Scanner
4. Health Check
5. Exit
""")

        choice = input("Select an option: ").strip()

        if choice == "1":
            start_scanner()
        elif choice == "2":
            stop_scanner()
        elif choice == "3":
            restart_scanner()
        elif choice == "4":
            health_check()
        elif choice == "5":
            print("Exiting.")
            stop_scanner()
            sys.exit(0)
        else:
            print(f"{YELLOW}[!] Invalid selection{RESET}")

        time.sleep(1)


if __name__ == "__main__":
    os.chdir(PROJECT_ROOT)
    menu()
