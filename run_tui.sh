#!/bin/bash
set -e

# Activate venv if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

python3 main.py
