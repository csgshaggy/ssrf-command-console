#!/bin/bash

while true; do
    clear
    echo "=== SSRF Console Ops Menu ==="
    echo "1) Status"
    echo "2) Restart services"
    echo "3) Tail backend logs"
    echo "4) Tail frontend logs"
    echo "5) Health check"
    echo "6) Uninstall services"
    echo "q) Quit"
    echo
    read -rp "Select option: " choice

    case "$choice" in
        1) ./status_services.sh; read -rp "Press Enter to continue..." ;;
        2) ./restart_services.sh; read -rp "Press Enter to continue..." ;;
        3) ./logs_backend.sh ;;
        4) ./logs_frontend.sh ;;
        5) ./health_check.sh; read -rp "Press Enter to continue..." ;;
        6) ./uninstall_services.sh; read -rp "Press Enter to continue..." ;;
        q|Q) exit 0 ;;
        *) echo "Invalid choice"; sleep 1 ;;
    esac
done
