from typing import List
from ssrf_scanner.utils.logger import get_logger
from ssrf_scanner.utils.http_helpers import send_http_probe
from ssrf_scanner.utils.result_models import ProbeResult

logger = get_logger("scanner_core")


def build_url(ip: str, port: int, path: str) -> str:
    """
    Construct a full URL from IP, port, and path.
    """
    if port == 80:
        return f"http://{ip}{path}"
    elif port == 443:
        return f"https://{ip}{path}"
    else:
        return f"http://{ip}:{port}{path}"


def probe_target(ip: str, port: int, path: str) -> ProbeResult:
    """
    Perform a single HTTP probe and return a structured ProbeResult.
    """
    url = build_url(ip, port, path)
    logger.info(f"Probing {url}")

    raw = send_http_probe(url)

    result = ProbeResult(
        url=raw["url"],
        status=raw["status"],
        elapsed=raw["elapsed"],
        error=raw["error"],
        content_preview=raw["content"],
        headers=raw["headers"],
    )

    return result


def probe_ip_across_ports_and_paths(ip: str, ports: List[int], paths: List[str]) -> List[ProbeResult]:
    """
    Probe a single IP across multiple ports and paths.
    Returns a list of ProbeResult objects.
    """
    results = []

    for port in ports:
        for path in paths:
            result = probe_target(ip, port, path)
            results.append(result)

    return results
from ssrf_scanner.paths import PATHS
from ssrf_scanner.ports import PORTS


def scan_single_ip(ip: str):
    """
    High-level wrapper that scans a single IP across all ports and paths.
    Returns a structured dictionary of results.
    """
    try:
        probe_results = probe_ip_across_ports_and_paths(ip, PORTS, PATHS)

        # Convert ProbeResult objects into dictionaries
        serialized = [r.to_dict() for r in probe_results]

        return {
            "ip": ip,
            "results": serialized,
            "timing_anomalies": [],
            "clusters": {},
            "patterns": [],
            "redirects": []
        }

    except Exception as e:
        return {"error": str(e)}
