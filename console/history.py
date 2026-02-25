"""
history.py
Persistent history manager for the SSRF Command Console.

Stores:
- mode runs
- results
- analysis
- timestamps

Backed by: results/history.json
"""

import json
import os
from datetime import datetime
from pathlib import Path


class HistoryManager:

    def __init__(self, history_file="results/history.json"):
        self.history_path = Path(history_file)
        self.history = []

        # Ensure results directory exists
        self.history_path.parent.mkdir(parents=True, exist_ok=True)

        # Load existing history if present
        if self.history_path.exists():
            try:
                with open(self.history_path, "r") as f:
                    self.history = json.load(f)
            except Exception:
                self.history = []

    # -------------------------------------------------------------
    # ADD ENTRY
    # -------------------------------------------------------------
    def add(self, mode_name, result, analysis):
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "mode": mode_name,
            "result": result,
            "analysis": analysis
        }

        self.history.append(entry)
        self.save()

    # -------------------------------------------------------------
    # SAVE TO DISK
    # -------------------------------------------------------------
    def save(self):
        try:
            with open(self.history_path, "w") as f:
                json.dump(self.history, f, indent=4)
        except Exception as e:
            print(f"[History] Failed to save: {e}")

    # -------------------------------------------------------------
    # GET ALL ENTRIES
    # -------------------------------------------------------------
    def all(self):
        return self.history

    # -------------------------------------------------------------
    # GET ENTRY BY INDEX
    # -------------------------------------------------------------
    def get(self, index):
        try:
            return self.history[index]
        except:
            return None
