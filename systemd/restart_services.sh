#!/bin/bash
set -e

echo "[+] Restarting SSRF backend..."
sudo systemctl restart ssrf-backend.service

echo "[+] Restarting SSRF frontend..."
sudo systemctl restart ssrf-frontend.service

echo "[✓] Restart complete."

echo
echo "[Status]"
sudo systemctl --no-pager --full status ssrf-backend.service | sed -n '1,8p'
echo
sudo systemctl --no-pager --full status ssrf-frontend.service | sed -n '1,8p'
