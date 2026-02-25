from typing import List, Dict
from ssrf_scanner.utils.result_models import ProbeResult

def classify_error_patterns(results: List[ProbeResult]) -> List[Dict]:
    """
    Classifies common error patterns such as timeouts, connection errors,
    empty responses, and HTTP error codes.
    """
    classifications = []

    for r in results:
        if r.is_timeout():
            classifications.append({"url": r.url, "pattern": "timeout"})
        elif r.is_connection_error():
            classifications.append({"url": r.url, "pattern": "connection_error"})
        elif r.status and 400 <= r.status < 500:
            classifications.append({"url": r.url, "pattern": f"http_{r.status}"})
        elif r.status and 500 <= r.status < 600:
            classifications.append({"url": r.url, "pattern": f"http_{r.status}"})
        elif r.is_empty():
            classifications.append({"url": r.url, "pattern": "empty_response"})
        else:
            classifications.append({"url": r.url, "pattern": "normal"})

    return classifications
