#!/bin/bash
set -e

# Start backend in new terminal
gnome-terminal -- bash -c "./run_backend.sh; exec bash"

# Start TUI in current terminal
./run_tui.sh
