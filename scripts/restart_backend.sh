#!/bin/bash

echo "[+] Killing all uvicorn + watchfiles processes..."
pkill -f uvicorn
pkill -f watchfiles

echo "[+] Waiting for port 8000 to clear..."
while sudo ss -tulpn | grep -q ":8000"; do
    sleep 0.2
done

echo "[+] Starting backend..."
source venv/bin/activate
uvicorn dashboard_web:app --reload --host 0.0.0.0 --port 8000
