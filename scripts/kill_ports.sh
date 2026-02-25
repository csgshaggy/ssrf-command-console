#!/bin/bash

PORTS=("8000" "8001" "8080" "5000")
LOGFILE="logs/kill_ports.log"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

mkdir -p logs

echo "[$TIMESTAMP] --- Multi-Port Kill Started ---" | tee -a "$LOGFILE"

for PORT in "${PORTS[@]}"; do
    echo "[*] Checking port $PORT..." | tee -a "$LOGFILE"
    PIDS=$(lsof -t -i :$PORT)

    if [ -z "$PIDS" ]; then
        echo "[+] No processes on port $PORT." | tee -a "$LOGFILE"
        continue
    fi

    echo "[!] Processes on port $PORT: $PIDS" | tee -a "$LOGFILE"

    FILTERED=""
    for PID in $PIDS; do
        CMD=$(ps -p $PID -o comm=)
        if [[ "$CMD" == "uvicorn" || "$CMD" == "python3" || "$CMD" == "python" ]]; then
            FILTERED="$FILTERED $PID"
        else
            echo "[!] Skipping non-Python PID $PID ($CMD)" | tee -a "$LOGFILE"
        fi
    done

    if [ -z "$FILTERED" ]; then
        echo "[!] No safe PIDs to kill on $PORT." | tee -a "$LOGFILE"
        continue
    fi

    echo "[*] Graceful kill on $PORT..." | tee -a "$LOGFILE"
    for PID in $FILTERED; do kill $PID 2>/dev/null; done
    sleep 0.5

    REMAIN=$(lsof -t -i :$PORT)
    if [ -n "$REMAIN" ]; then
        echo "[*] Force kill on $PORT: $REMAIN" | tee -a "$LOGFILE"
        for PID in $REMAIN; do kill -9 $PID 2>/dev/null; done
    fi

    FINAL=$(lsof -t -i :$PORT)
    if [ -z "$FINAL" ]; then
        echo "[+] Port $PORT cleared." | tee -a "$LOGFILE"
    else
        echo "[!] WARNING: Still busy: $FINAL" | tee -a "$LOGFILE"
    fi
done

echo "[$TIMESTAMP] --- Multi-Port Kill Completed ---" | tee -a "$LOGFILE"
