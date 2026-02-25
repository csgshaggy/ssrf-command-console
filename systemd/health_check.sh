#!/bin/bash

BACKEND_URL="http://127.0.0.1:5001"
FRONTEND_URL="http://127.0.0.1:8080"

echo "=== SSRF Console Health Check ==="
echo

echo "[+] Checking backend: $BACKEND_URL"
if curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL" | grep -qE '200|302|301'; then
    echo "    Backend reachable."
else
    echo "    Backend NOT healthy (non-2xx/3xx)."
fi

echo
echo "[+] Checking frontend: $FRONTEND_URL"
if curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL" | grep -qE '200|302|301'; then
    echo "    Frontend reachable."
else
    echo "    Frontend NOT healthy (non-2xx/3xx)."
fi

echo
echo "[+] Systemd service summary:"
systemctl is-active ssrf-backend.service ssrf-frontend.service
