#!/bin/bash

set -e

echo "[+] Creating /etc/ssrf directory..."
sudo mkdir -p /etc/ssrf

echo "[+] Copying environment file..."
sudo cp ssrf.env /etc/ssrf/ssrf.env
sudo chmod 600 /etc/ssrf/ssrf.env

echo "[+] Installing systemd service files..."
sudo cp ssrf-backend.service /etc/systemd/system/
sudo cp ssrf-frontend.service /etc/systemd/system/

echo "[+] Reloading systemd..."
sudo systemctl daemon-reload

echo "[+] Enabling services..."
sudo systemctl enable ssrf-backend.service
sudo systemctl enable ssrf-frontend.service

echo "[+] Starting services..."
sudo systemctl start ssrf-backend.service
sudo systemctl start ssrf-frontend.service

echo "[✓] Installation complete."
