#!/bin/bash
set -e

echo "[+] Stopping services..."
sudo systemctl stop ssrf-backend.service || true
sudo systemctl stop ssrf-frontend.service || true

echo "[+] Disabling services..."
sudo systemctl disable ssrf-backend.service || true
sudo systemctl disable ssrf-frontend.service || true

echo "[+] Removing service files..."
sudo rm -f /etc/systemd/system/ssrf-backend.service
sudo rm -f /etc/systemd/system/ssrf-frontend.service

echo "[+] Reloading systemd..."
sudo systemctl daemon-reload

echo "[+] Removing /etc/ssrf env directory (optional)..."
sudo rm -rf /etc/ssrf

echo "[✓] Uninstall complete."
