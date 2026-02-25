# scripts/checks/baseline_snapshot.py

import json
import os
from datetime import datetime


def ensure_baseline_dirs(base_dir, current_dir, history_dir):
    os.makedirs(base_dir, exist_ok=True)
    os.makedirs(current_dir, exist_ok=True)
    os.makedirs(history_dir, exist_ok=True)


def _write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def save_baseline_snapshot(agg_data, current_dir, history_dir, timestamp=None):
    if timestamp is None:
        timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")

    # Save current baseline
    _write_json(os.path.join(current_dir, "baseline.json"), agg_data)

    # Save timestamped history snapshot
    snap_dir = os.path.join(history_dir, timestamp)
    os.makedirs(snap_dir, exist_ok=True)
    _write_json(os.path.join(snap_dir, "baseline.json"), agg_data)


def load_current_baseline(current_dir):
    path = os.path.join(current_dir, "baseline.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
