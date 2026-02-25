#!/bin/bash

PORT=8000
LOGFILE="logs/kill_port.log"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

mkdir -p logs

echo "[$TIMESTAMP] --- Kill Script Started (Port $PORT) ---" | tee -a "$LOGFILE"

# Find PIDs bound to the port
PIDS=$(lsof -t -i :$PORT)

if [ -z "$PIDS" ]; then
    echo "[+] No processes found on port $PORT." | tee -a "$LOGFILE"
    exit 0
fi

echo "[!] Processes detected on port $PORT: $PIDS" | tee -a "$LOGFILE"

# Filter only uvicorn/python processes (safety)
FILTERED_PIDS=""
for PID in $PIDS; do
    CMD=$(ps -p $PID -o comm=)
    if [[ "$CMD" == "uvicorn" || "$CMD" == "python3" || "$CMD" == "python" ]]; then
        FILTERED_PIDS="$FILTERED_PIDS $PID"
    else
        echo "[!] Skipping non-Python process: PID $PID ($CMD)" | tee -a "$LOGFILE"
    fi
done

if [ -z "$FILTERED_PIDS" ]; then
    echo "[!] No safe processes to kill." | tee -a "$LOGFILE"
    exit 1
fi

echo "[*] Attempting graceful termination..." | tee -a "$LOGFILE"
for PID in $FILTERED_PIDS; do
    kill $PID 2>/dev/null
done

sleep 0.5

# Check again
REMAINING=$(lsof -t -i :$PORT)

if [ -z "$REMAINING" ]; then
    echo "[+] All processes terminated cleanly." | tee -a "$LOGFILE"
else
    echo "[!] Remaining processes: $REMAINING" | tee -a "$LOGFILE"
    echo "[*] Forcing termination..." | tee -a "$LOGFILE"

    for PID in $REMAINING; do
        kill -9 $PID 2>/dev/null
    done
fi

sleep 0.3

FINAL=$(lsof -t -i :$PORT)

if [ -z "$FINAL" ]; then
    echo "[+] Port $PORT is now fully free." | tee -a "$LOGFILE"
else
    echo "[!] WARNING: Some processes could not be killed: $FINAL" | tee -a "$LOGFILE"
fi

echo "[$TIMESTAMP] --- Kill Script Completed ---" | tee -a "$LOGFILE"
