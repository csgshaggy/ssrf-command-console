#!/bin/bash
set -e

echo "=== SSRF Backend Status ==="
sudo systemctl --no-pager --full status ssrf-backend.service | sed -n '1,12p'

echo
echo "=== SSRF Frontend Status ==="
sudo systemctl --no-pager --full status ssrf-frontend.service | sed -n '1,12p'
