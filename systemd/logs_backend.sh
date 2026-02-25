#!/bin/bash

echo "[+] Tailing backend logs (Ctrl+C to exit)..."
sudo journalctl -u ssrf-backend.service -f -n 100
