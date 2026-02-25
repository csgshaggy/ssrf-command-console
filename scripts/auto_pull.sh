#!/bin/bash

WATCH_REMOTE="origin/main"
LOCAL_DIR="/home/kali/SSRF_CONSOLE"

while true; do
    cd "$LOCAL_DIR"
    git fetch origin

    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse $WATCH_REMOTE)

    if [ "$LOCAL" != "$REMOTE" ]; then
        echo "Remote updated — pulling changes..."
        git pull
    fi

    sleep 10
done
