from typing import List
from ssrf_scanner.utils.result_models import ProbeResult

def detect_timing_anomalies(results: List[ProbeResult], threshold_factor: float = 2.0):
    """
    Detects timing anomalies by comparing each probe's response time
    to the average across all probes.
    """
    if not results:
        return []

    avg = sum(r.elapsed for r in results) / len(results)
    anomalies = []

    for r in results:
        if r.elapsed > avg * threshold_factor:
            anomalies.append({
                "url": r.url,
                "elapsed": r.elapsed,
                "avg": avg,
                "reason": "timing_anomaly"
            })

    return anomalies
