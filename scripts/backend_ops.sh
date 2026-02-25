#!/bin/bash

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOGFILE="../logs/backend_ops.log"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

mkdir -p ../logs

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOGFILE"
}

run_script() {
    local script="$SCRIPTS_DIR/$1"
    if [ ! -f "$script" ]; then
        log "[ERROR] Script not found: $script"
        return
    fi
    bash "$script"
}

backend_status() {
    echo
    echo "[ Backend Status ]"
    PIDS=$(lsof -t -i :8000)
    if [ -z "$PIDS" ]; then
        echo "[-] Backend NOT running on port 8000"
    else
        echo "[+] Backend running on port 8000"
        echo "    PIDs: $PIDS"
    fi
}

show_menu() {
    clear
    echo "========================================="
    echo "         SSRF Console Backend Ops        "
    echo "========================================="
    echo "1) Backend status"
    echo "2) Kill backend (port 8000)"
    echo "3) Kill + restart backend"
    echo "4) Kill multiple ports (8000, 8001, 8080, 5000)"
    echo "5) View backend logs"
    echo "6) Exit"
    echo "-----------------------------------------"
}

view_logs() {
    LOG="../logs/kill_port.log"
    if [ ! -f "$LOG" ]; then
        echo "[!] No log file found at $LOG"
        return
    fi
    echo
    echo "----- Last 200 lines of backend logs -----"
    tail -n 200 "$LOG"
    echo "-------------------------------------------"
}

while true; do
    show_menu
    read -p "> " choice

    case "$choice" in
        1)
            backend_status
            read -p "Press Enter to continue..."
            ;;
        2)
            log "Killing backend..."
            run_script "kill_port.sh"
            read -p "Press Enter to continue..."
            ;;
        3)
            log "Killing + restarting backend..."
            run_script "kill_and_restart.sh"
            read -p "Press Enter to continue..."
            ;;
        4)
            log "Killing multiple ports..."
            run_script "kill_ports.sh"
            read -p "Press Enter to continue..."
            ;;
        5)
            view_logs
            read -p "Press Enter to continue..."
            ;;
        6)
            log "Exiting backend ops menu."
            exit 0
            ;;
        *)
            echo "[!] Invalid option"
            sleep 1
            ;;
    esac
done
