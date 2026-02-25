from typing import List, Dict
from ssrf_scanner.utils.result_models import ProbeResult

def detect_redirects(results: List[ProbeResult]) -> List[Dict]:
    """
    Detects HTTP redirects (301, 302, 307, 308) and extracts the Location header.
    """
    redirects = []

    for r in results:
        if r.status in (301, 302, 307, 308):
            redirects.append({
                "url": r.url,
                "status": r.status,
                "location": r.headers.get("Location", None)
            })

    return redirects
