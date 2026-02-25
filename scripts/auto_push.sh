#!/bin/bash

WATCH_DIR="/home/kali/SSRF_CONSOLE"

inotifywait -m -r -e modify,create,delete,move "$WATCH_DIR" |
while read path action file; do
    cd "$WATCH_DIR"
    git add .
    git commit -m "Auto-sync: $action $file at $(date)"
    git push
done
