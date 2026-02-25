#!/bin/bash

echo "🧹 Cleaning obsolete SSRF Console files..."

# Delete old logs
rm -f backend.log
rm -f frontend.log

# Delete old dashboard scripts
rm -f dashboard.py
rm -f dashboard_tui.py
rm -f start_dashboard.sh

# Delete old manager
rm -f ssrf_manager.py

# Delete Python cache
rm -rf __pycache__

# Optional: delete requirements.txt if you want the package to manage deps
# rm -f requirements.txt

echo "✔ Cleanup complete. Your SSRF Console is now tidy and modular."
