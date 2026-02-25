#!/bin/bash

PORT=8000
LOGFILE="logs/kill_port.log"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

mkdir -p logs

echo "[$TIMESTAMP] --- Kill + Restart Script Started (Port $PORT) ---" | tee -a "$LOGFILE"

# Find PIDs bound to the port
PIDS=$(lsof -t -i :$PORT)

if [ -z "$PIDS" ]; then
    echo "[+] No processes found on port $PORT." | tee -a "$LOGFILE"
else
    echo "[!] Processes detected on port $PORT: $PIDS" | tee -a "$LOGFILE"

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
    else
        echo "[*] Attempting graceful termination..." | tee -a "$LOGFILE"
        for PID in $FILTERED_PIDS; do
            kill $PID 2>/dev/null
        done

        sleep 0.5

        REMAINING=$(lsof -t -i :$PORT)
        if [ -n "$REMAINING" ]; then
            echo "[!] Forcing termination of remaining processes: $REMAINING" | tee -a "$LOGFILE"
            for PID in $REMAINING; do
                kill -9 $PID 2>/dev/null
            done
        fi
    fi
fi

sleep 0.3

FINAL=$(lsof -t -i :$PORT)
if [ -n "$FINAL" ]; then
    echo "[!] WARNING: Some processes could not be killed: $FINAL" | tee -a "$LOGFILE"
    exit 1
fi

echo "[+] Port $PORT is now free. Restarting backend..." | tee -a "$LOGFILE"

nohup uvicorn app.main:app --reload > logs/backend_restart.log 2>&1 &

NEWPID=$!
echo "[+] Backend restarted with PID $NEWPID" | tee -a "$LOGFILE"
echo "[$TIMESTAMP] --- Kill + Restart Completed ---" | tee -a "$LOGFILE"
