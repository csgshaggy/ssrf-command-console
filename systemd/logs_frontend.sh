#!/bin/bash

echo "[+] Tailing frontend logs (Ctrl+C to exit)..."
sudo journalctl -u ssrf-frontend.service -f -n 100
