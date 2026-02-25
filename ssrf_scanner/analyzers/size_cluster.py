from typing import List, Dict
from ssrf_scanner.utils.result_models import ProbeResult

def cluster_by_response_size(results: List[ProbeResult]) -> Dict[str, List[ProbeResult]]:
    """
    Groups responses by approximate content size.
    Helps identify outliers that may indicate interesting services.
    """
    clusters = {
        "empty": [],
        "small": [],
        "medium": [],
        "large": [],
    }

    for r in results:
        size = len(r.content_preview)

        if size == 0:
            clusters["empty"].append(r)
        elif size < 200:
            clusters["small"].append(r)
        elif size < 2000:
            clusters["medium"].append(r)
        else:
            clusters["large"].append(r)

    return clusters
