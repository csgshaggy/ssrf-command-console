.PHONY: tui backend all clean

tui:
	python3 main.py

backend:
	python3 run_uvicorn.py

all:
	@echo "Starting backend..."
	@gnome-terminal -- bash -c "./run_backend.sh; exec bash"
	@echo "Starting TUI..."
	@./run_tui.sh

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
