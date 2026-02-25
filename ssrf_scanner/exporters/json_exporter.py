import json
from typing import Any, Dict

def export_results_to_json(data: Dict[str, Any], filepath: str):
    """
    Writes scan results to a JSON file.
    """
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, default=str)
