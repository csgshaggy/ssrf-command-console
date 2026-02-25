#!/bin/bash
set -e

if [ -d "venv" ]; then
    source venv/bin/activate
fi

python3 run_uvicorn.py
